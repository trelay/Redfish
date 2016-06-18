#!/usr/bin/python3
import configparser

url_dict={"@Redfish.Copyright":"Copyright @ 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.","@odata.context":"","@odata.id":"/redfish/v1/Systems/123fed3029c-b23394-12/Memory/13","@odata.type":"#Memory.1.0.0.Memory","Id":"13","Name":"MemoryModule","Manufacturer":"","Socket":"13","Bank":"","Type":"DDR-3 RAM","SizeGB":16,"SpeedMHz":1600,"VoltageVolt":1.35,"DataWidthBits":0,"TotalWidthBits":0,"FormFactor":"DIMM","SerialNumber":"","AssetTag":"","PartNumber":"","Rank":"","ConfiguredSpeedMHz":0,"MinimumVoltageVolt":0,"MaximumVoltageVolt":0,"Status":{"State":"Enabled","Health":"OK"},"Location":{"Pod":1,"Rack":1,"Drawer":1,"Module":0,"Blade":123},"Oem":{},"Links":{"ContainedBy":{"@odata.id":"/redfish/v1/Systems/123fed3029c-b23394-12"},"Oem":{}}}

class Reponse_check(object):
	def __init__(self):
		self.url_dict=url_dict
		self.conf_file=conf_file
	
	def confcompare(self,url_dict,conf_file):
		conf = configparser.ConfigParser()
		conf.optionxform = str
		conf.read(self.conf_file)
		current_url_name=self.url_dict["Name"]
		for opt,value in conf[current_url_name].items():
			if opt in self.url_dict:
				if str(url_dict[opt])==value.strip():
					print("{0:s}: Value mathced for key: {1:s}"\
						.format(current_url_name,opt))
				else:
					print("{0:s}: Value mismatched for key: {1:s}"\
						.format(current_url_name,opt))
			else:
				print("{0:s}: Can't find {1:s} in response, check config"\
						.format(current_url_name,opt))
	def request_time_check(self, request_time):
		if request_time>CONF.REQUEST.http_time:
			msg="RESTful Server takes too long to respond URL:{0:s}"\
				.format(self.url)
			logger.warn(msg)

#confcompare(url_dict,"url_dict.conf")
Req_check=Reponse_check(0,url_dict,"url_dict.conf")
Req_check.confcompare()
