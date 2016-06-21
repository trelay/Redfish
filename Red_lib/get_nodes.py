#!/usr/bin/python3
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
from datetime import datetime
from datetime import timedelta
import socket 
import json
from distutils.version import LooseVersion

from Red_lib.loglib import logger
from Red_lib.Red_Error import HttpTimeError
from Red_lib.retry import retry
from Red_lib.config import CONF
import os.path
import configparser

socket.setdefaulttimeout(CONF.REQUEST.timeout)
VERSION = '1.0.0'

class GEN_URL():
	'''
	Build complete URL

	:param host: IP address or domain name of the target 
		Rest Server's resource interface.
	:type host: str
	:param path: the path of the URL to access a specific Redfish Node.
		example:'/redfish/v1'
	:type path: str, optional
	:param url: the url of a specific Redfish Node.
		example:'http://10.204.29.221:8888/redfish/v1/Managers/1'
	:type url: str, optional

	:output get_url: return completed URL to access a specific node.
	:type get_url: str
	:output get_path: return path of an URL.
	:type get_url: str
	'''
	supported_rest_versions = CONF.REST.ver_support

	def __init__(self,host,scheme='http',rest_version=None):
		self._empty_com=urllib.parse.urlparse('')
		self._scheme=scheme
		port=str(CONF.REST.bind_port)
		self._netloc=host+":"+port
		self.cli_name = CONF.REST.client_name
		self._rest_version = rest_version
		self.new_url=''

	def _check_rest_version(self, version):
		"""Validate a REST API version is supported by the library and target array."""
		version = str(version)
		if version not in self.supported_rest_versions:
			msg = "Library is incompatible with REST API version {0}"
			raise ValueError(msg.format(version))
		return version

	def _choose_rest_version(self):
		"""Return the latest REST API version supported by target array."""
		return max(self.supported_rest_versions, key=LooseVersion)

	def _gen_rest_ver(self):
		if self._rest_version:
			# check input version whether is in support list
			self._rest_version = self._check_rest_version(rest_version)
		else:
			self._rest_version = self._choose_rest_version()

	def get_url(self, path=None):
		if path == None:
			self._gen_rest_ver()
			path="/{0}/v{1}".format(self.cli_name, self._rest_version)

		new_url_obj=self._empty_com._replace(scheme='http', netloc=self._netloc,path=path)
		self.new_url= new_url_obj.geturl()
		return self.new_url

	def get_path(self,url=None):
		if url==None:
			url=self.new_url
		return urllib.parse.urlparse(url).path

#url=GEN_URL('10.204.29.221')
#print(url.get_url('/redfish/v2')

class GET_NODE(object):
	def __init__(self,host):
		self.host=host
		self.url_list=[]

	def scan_node(self,node_path=None):
		url_obj=GEN_URL(self.host)
		node_url=url_obj.get_url(node_path)
		
		#if node_path==None:
		#	node_path=self.root_path
		# Pick valid URL
		if CONF.REST.client_name in node_url:
			self.url_list.append(node_url)
			for sub_node_path in self.__get_sub_node(node_url):
				#sub_node_url=url_obj.get_url(sub_node_path)
				if sub_node_path != "":
					self.scan_node(sub_node_path)

	def __odata_phaser(self,url_dict):
		sub_node_path_list=[]
		for node_name in url_dict:
			node_property=url_dict[node_name]
			if isinstance(node_property,dict):
				for node_pro_key in node_property:
					if '@odata.id'==node_pro_key:
						sub_node_path_list.append(node_property[node_pro_key])
		return sub_node_path_list
						
	
	def __number_phaser(self,url_dict):
		sub_node_path_list=[]
		if "Members@odata.count" in url_dict and isinstance(url_dict,dict):
			for odata_dict in url_dict["Members"]:
				sub_node_path_list.append(odata_dict["@odata.id"])
		return sub_node_path_list
	
	def __get_sub_node(self,node_url):
	#def get_sub_node(self,node_url):
		url_request=URL_REQUEST(node_url)
		url_request.get_req()
		url_dict=url_request.response_dict

		sub_node_path_list=[]
		if len(url_dict)>0:
			sub_node_path_list= self.__number_phaser(url_dict)+ \
								self.__odata_phaser(url_dict)
		return sub_node_path_list
		
def Send_Auth(url,username,password):
	if not (username and password):
		raise ValueError("Must specify both username and password, \
				as Server asks Authentication!")
	password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, url, username, password)
	
	authhandler = urllib.request.HTTPBasicAuthHandler(password_mgr)
	opener = urllib.request.build_opener(authhandler)
	#opener.open(url)
	urllib.request.install_opener(opener)

class URL_REQUEST():

	def __init__(self,url,username=None, password=None):
		if CONF.REST.client_name not in url:
			raise ValueError("Not a valid redfish URL")
		self.response_dict={}
		self.url=url.strip().replace(" ", "%20")
		self.response_check=Reponse_check()

	@retry((HTTPError,socket.timeout,URLError,ValueError), 
			tries=CONF.REQUEST.retries, delay=CONF.REQUEST.delay,
			backoff=CONF.REQUEST.backoff, stoponerror=CONF.REQUEST.failonerror,
			logger=logger)

	def get_req(self,values=None):
		if values:
			if not isinstance(values,dict):
				raise TypeError("POST data should be a python dict")
			else:
				msg="POST: Attempting to request URL: {0}".format(self.url)
				data = urllib.parse.urlencode(values)
				data = data.encode('ascii') # data should be bytes
				req = urllib.request.Request(self.url, data)
		else:
			msg="GET: Attempting to request URL: {0}".format(self.url)
			req = urllib.request.Request(self.url)
		logger.info(msg)

		try:
			start_time=datetime.now()
			response = urllib.request.urlopen(req)
			#Need close the urlopen here??? or just run Burn-in
		except URLError as ue:
			if hasattr(ue,'reason'):
				msg='Failed to reach the server: {0}.'.format(ue.reason)
				logger.error(msg)
			elif hasattr(ue,'code'):
				msg='The server couldn\'t fulfill the request. Error code{0}'\
					.format(ue.code)
				logger.error(msg)
				if ue.code==401:
					Send_Auth(self.url,username,password)
			raise
		else:
			end_time=datetime.now()
			data=response.read().decode('utf-8')
			#To run Burn-in test, keep response.close() commented
			#response.close()

			request_time=(end_time-start_time).total_seconds()
			msg="Spent {0:6f}s to get response from {1:s}"\
				.format(request_time,self.url)
			logger.info(msg)
			self.response_check.request_time_check(request_time,self.url)

		try:
			self.response_dict=json.loads(data)
		except ValueError as ve:
			msg="Get invaild feedback from RESTful server when open URL:{0}, \
				infor:{1}".format(self.url,data)
			logger.error(msg)
			raise
		self.response_check.confcompare(self.response_dict,CONF.MAIN.value_file)
		return self.response_dict

class Reponse_check(object):
	def __init__(self):
		pass
	
	def confcompare(self, url_dict, conf_file):
		if not os.path.isfile(conf_file):
			msg='Didn\'t find compare files to check the response data.'
			logger.warn(msg)
		conf = configparser.ConfigParser()
		conf.optionxform = str
		conf.read(conf_file)
		current_url_name=url_dict["Name"]
		if current_url_name in conf:
			for opt,value in conf[current_url_name].items():
				if opt in url_dict:
					if str(url_dict[opt])==value.strip():
						msg="{0}: Value mathced for key: {1}, got: {2}"\
							.format(current_url_name,opt, value.strip())
						logger.info(msg)
					else:
						msg="{0}: Value mismatched for key: {1}, expect: {2}, got: {3}"\
							.format(current_url_name,opt, value.strip(),str(url_dict[opt]))
						logger.error(msg)
				else:
					msg="{0}: Can't find key: {1} in response data, check config"\
							.format(current_url_name,opt)
					logger.error(msg)
	def request_time_check(self, request_time,url):
		if request_time>CONF.REQUEST.http_time:
			msg="RESTful Server takes too long to respond URL:{0}"\
				.format(url)
			logger.warn(msg)
