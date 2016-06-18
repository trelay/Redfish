#!/usr/bin/python3
from Red_lib.config import CONF
import os

cfg_file=os.path.join(os.path.split(os.path.abspath(__file__))\
						[0],'Redfish.conf')
value_file=os.path.join(os.path.split(os.path.abspath(__file__))\
						[0],'Red_lib/product/url_dict.conf')
logfilename=os.path.splitext(os.path.abspath(__file__))[0]+".log"
CONF.set_override(name='cfg_file', override=cfg_file)
CONF.set_override(name='value_file', override=value_file)
CONF.set_override(name='logfilename', override=logfilename, group='LOG')

from urllib.request import urlopen
import json
from time import sleep
from Red_lib.loglib import logger
from Red_lib.get_nodes import GET_NODE, URL_REQUEST

CONF(default_config_files=[CONF.cfg_file])

host = "10.204.29.201"
#host = "10.204.29.104"
#url = "/redfish/v1/Systems/Default string"
url = "/redfish/v1"

def compare_url(last_url=None,new_url=None):
	diff_url_str=""

	if len(last_url)<len(new_url):
		for url in list(set(new_url)-set(last_url)):
			diff_url_str+="\n\t"+url
		msg="New node has been found:{0:s}".format(diff_url_str)
	else:
		for url in list(set(last_url)-set(new_url)):
			diff_url_str+="\n\t"+url
		msg="Missed node:{0:s}".format(diff_url_str)

	logger.warn(msg)
	
def main():
	for i in range(CONF.cycle):
		msg="SCAN ALL THE NODES IN CYCLE: {0:d}".format(i)
		logger.info(msg)
		get_node=GET_NODE(host)
		get_node.scan_node()
		new_url=get_node.url_list

		if i!=0:
			if last_url!=new_url:
				compare_url(last_url,new_url)

		last_url=new_url
		#input("Press Enter to continue...")

if __name__=="__main__":
	main()
	#pass
	



'''

xxx=GET_NODE(host)
xxx.scan_node()
print("sleep 5")
sleep(5)

for i in range(3):
	for node_url in xxx.url_list:
		url_request=URL_REQUEST(node_url)
		res_dict=url_request.get_req()
		print(res_dict['Name'])
		print(res_dict['@odata.id']+"\n")
		sleep(0.3)
	

def get_next_node(url):
	response=urlopen(self.host_port+self.url)
	data = response.read().decode('utf-8')
	
	
	
	

print('\n')
print(root_dict)
print('\n')
print("parent URI:"+root_dir["@odata.id"])
print('\n')
for key in root_dir:
	value=root_dir[key]
	if isinstance(value,dict):
		print(key+":"+str(value))
'''
