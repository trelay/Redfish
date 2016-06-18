#!/usr/bin/python3
import unittest
import sys
from unittest import mock
from socket import timeout
from urllib.request import urlopen
sys.path.append('/root/Redfish_r/')
from Red_lib.get_nodes import GEN_URL,URL_REQUEST,GET_NODE
from config import CONF
#from Red_lib import get_nodes
#available host: 10.204.29.221
url_dict= {"@Redfish.Copyright":"Copyright @ 2014-2015 Distributed Management Task Force, Inc. (DMTF). All rights reserved.","@odata.context":"/redfish/v1/$metadata#Systems/Members/$entity","@odata.id":"/redfish/v1/Systems/Default string","@odata.type":"#ComputerSystem.1.0.0.ComputerSystem","Id":"Default string","Name":"CS3","SystemType":"Physical","AssetTag":"","Manufacturer":"Default string","Model":"Default string","SKU":"","SerialNumber":"Default string","PartNumber":"Default string","Description":"","UUID":"6e1021ec-266a-11e6-be4b-1b6768cbe68d","HostName":"cls-cs3","Status":{"State":"Enabled","Health":"OK"},"IndicatorLED":"","PowerState":"On","Boot":{"BootSourceOverrideEnabled":"Disabled","BootSourceOverrideTarget":"None","BootSourceOverrideTarget@DMTF.AllowableValues":["None","Pxe","Hdd"],"UefiTargetBootSourceOverride":""},"BiosVersion":"5.11","ProcessorSummary":{"Status":{"State":"Enabled","Health":"OK","HealthRollup":"OK"},"Count":2,"ProcessorFamily":""},"MemorySummary":{"Status":{"State":"Enabled","Health":"OK","HealthRollup":"OK"},"TotalSystemMemoryGB":64},"Processors":{"@odata.id":"/redfish/v1/Systems/Default string/Processors"},"EthernetInterfaces":{"@odata.id":"/redfish/v1/Systems/Default string/EthernetInterfaces"},"Memory":{"@odata.id":"/redfish/v1/Systems/Default string/Memory"},"LogServices":{"@odata.id":"/redfish/v1/Systems/Default string/LogServices"},"Links":{"Processors":{"@odata.id":"/redfish/v1/Systems/Default string/Processors"},"Memory":{"@odata.id":"/redfish/v1/Systems/Default string/Memory"},"Chassis":[],"EthernetInterfaces":{"@odata.id":"/redfish/v1/Systems/Default string/EthernetInterfaces"},"ManagedBy":[{"@odata.id":"/redfish/v1/Managers/1"}],"Oem":{}},"Actions":{"#ComputerSystem.Reset":{"target":"/redfish/v1/Systems/Default string/Actions/ComputerSystem.Reset","ResetType@DMTF.AllowableValues":["On","ForceOff","SoftShutdown"]}},"Oem":{"Contoso":{"@odata.type":"http://Contoso.com/Schema#Contoso.ComputerSystem","ProductionLocation":{"FacilityName":"PacWest ProductionFacility","Country":"USA"}},"Chipwise":{"@odata.type":"http://Chipwise.com/Schema#Chipwise.ComputerSystem","Style":"Executive"}},"ManagedBy":{"@odata.id":"/redfish/v1/Managers/1"}}

class TestStringMethods(unittest.TestCase):
	def setUp(self):
		#self.tgen_url = get_nodes.GEN_URL("192.168.0.1")
		self.tgen_url = GEN_URL("192.168.0.1")
		self.tget_node = GET_NODE("192.168.0.1")
		self.tget_req = URL_REQUEST("http://10.204.29.221:8888/redfish/v1")
	def tearDown(self):
		pass

	#def test_geturl(self):
	#	self.assertEqual(self.tgen_url.get_url(), "http://192.168.0.1:8888/redfish/v1")

	#def test_getpath(self):
	#	self.assertEqual(self.tgen_url.get_path("http://192.168.0.1:8888/redfish/v1"), "/redfish/v1")

	def test_getreq(self):
		success_send = mock.Mock(return_value=url_dict)
		URL_REQUEST.get_req = success_send
		print(self.tget_node.get_sub_node("redfish"))
		#self.assertEqual(self.tget_node.get_sub_node("redfish"), '200')
		#print(self.tget_req.get_req())
		#self.assertEqual(self.tget_node.get_sub_node("redfish"), '200')
	#	with self.assertRaises(timeout):
	#		self.tget_req.get_req()
	

if __name__ == '__main__':
	unittest.main()
