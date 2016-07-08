#!/usr/bin/python3
import argparse
from Red_lib.config import CONF
import os
import re
from datetime import datetime
from urllib.request import urlopen
import json
from time import sleep
from Red_lib.loglib import logger
from Red_lib.get_nodes import GET_NODE, URL_REQUEST
VERSION = '1.0.0'

host = "10.204.29.243"

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

	logger.warning(msg)
	
def main():
	for i in range(CONF.MAIN.cycle):
		msg="SCAN ALL THE NODES IN CYCLE: {0:d}".format(i)
		logger.info(msg)
		get_node=GET_NODE(host)
		get_node.scan_node()
		new_url=get_node.url_list

		if i!=0:
			if last_url!=new_url:
				compare_url(last_url,new_url)
		last_url=new_url

		if CONF.CLI.time_to_stop:
			if datetime.now()>datetime.strptime(CONF.CLI.time_to_stop,\
				 '%Y-%m-%d %H:%M:%S'):
				break
		#input("Press Enter to continue...")
	msg='Stop test on {0}, cycle {1}'.format(datetime.now(),(i+1))
	logger.info(msg)


if __name__=="__main__":
	main()
	#pass
