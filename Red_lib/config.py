#!/usr/bin/python3
from oslo.config import cfg
import os.path

def find_cfg_file():
	conf_list=['Redfish.conf','../Redfish.conf','../../Redfish.conf']
	for conf_file in conf_list:
		if os.path.isfile(conf_file):
			return conf_file
###############################################################
rest_group = cfg.OptGroup(
	name='REST', 
	title='RESTful group options'
)
rest_cfg_opts = [
	cfg.StrOpt(
		name='client_name',
		default='redfish',
		help='Client app name that communicates with resetful'),

	cfg.IntOpt(
		name='bind_port',
		default=8888,
		help='Port number the server listens on.'),

	cfg.ListOpt(
		name='ver_support',
		default=['1'],
		help='The ver of Redfish this app supports.')
]
###############################################################
main_group = cfg.OptGroup(
	name='MAIN', 
	title='MAIN group options'
)
main_cfg_opts = [
	cfg.StrOpt(
         name='value_file',
         default='/product/url_dict.conf',
         help='Path of comparing file'),
     cfg.IntOpt(
         name='cycle',
         default=2,
         help='cycle to execute.')
]
##########################################################3
log_group = cfg.OptGroup(
	name='LOG', 
	title='LOG group options'
)

log_cfg_opts = [

	cfg.StrOpt(
	name='app_name',
	default='redfish_test',
	help='APP name showed in Log'),

	cfg.StrOpt(
	name='logfilename',
	default='./redfish.log',
	#default=None,
	help='Log file path.'),

	cfg.StrOpt(
	name='log_format',
	default=None,
	help='Log format in log file.'),

	cfg.IntOpt(
	name='root_level',
	default=10,
	help='Log level for global.'),

	cfg.IntOpt(
	name='ch_level',
	default=10,
	help='Log level for console stream.'),

	cfg.IntOpt(
	name='fh_level',
	default=20,
	help='Log level for file stream.'),

]
##########################################################3
request_group = cfg.OptGroup(
	name='REQUEST',
	title='Request options'
)
req_fail_opts = [
	cfg.FloatOpt(
	name='http_time',
	default= 0.4,
	help='The limit of request time'),

	cfg.FloatOpt(
	name='timeout',
	default= 2.0,
	help='Timeout to request an URL'),

	cfg.IntOpt(
	name='retries',
	default= 8,
	help='How many times will retry after failure'),

	cfg.FloatOpt(
	name='delay',
	default= 1.5,
	help='How long will execute the next retry'),

	cfg.IntOpt(
	name='backoff',
	default= 2,
	help='backoff times will retry'),

	cfg.BoolOpt(
	name='failonerror',
	default=False,
	help="whether we need stop if occor error")
]

CONF = cfg.CONF
CONF.register_group(rest_group)
CONF.register_opts(rest_cfg_opts, rest_group)

CONF.register_group(main_group)
CONF.register_opts(main_cfg_opts, main_group)

CONF.register_group(log_group)
CONF.register_opts(log_cfg_opts, log_group)

CONF.register_group(request_group)
CONF.register_opts(req_fail_opts, request_group)
#Above: Add parsing .ini style configuration files
#Below: Add command line arguments:
CONF.register_cli_opt(cfg.IntOpt('retry', positional=False,
	help='Cycles to scan the nodes'))
CONF.register_cli_opt(cfg.StrOpt('logname', positional=False,
	help='Location for the execution log'))
CONF.register_cli_opt(cfg.StrOpt('comp_file', positional=False,
	help='The url response data compare file'))

CONF(default_config_files=[find_cfg_file()])

if CONF.retry:
	CONF.REQUEST.retries= CONF.retry
if CONF.logname:
	CONF.LOG.logfilename= CONF.logname
else:
	#Locate the axactly postion for redfish.log
	CONF.LOG.logfilename=os.path.join(os.path.dirname(\
		os.path.abspath(__file__)),'..',CONF.LOG.logfilename)
if CONF.comp_file:
	CONF.MAIN.value_file= CONF.comp_file


if __name__ =="__main__":
	print('CONF.value_file',CONF.MAIN.value_file)
	print('CONF.MAIN.cycle',CONF.MAIN.cycle)
	print('CONF.client_name:',CONF.REST.client_name)
	print('CONF.bind_port:',CONF.REST.bind_port)
	print('CONF.ver_support:',CONF.REST.ver_support)
	print('CONF.LOG.app_name:',CONF.LOG.app_name)
	print('CONF.LOG.logfilename:',CONF.LOG.logfilename)
	print('CONF.LOG.log_format:',CONF.LOG.log_format)
	print('CONF.LOG.root_level:',CONF.LOG.root_level)
	print('CONF.LOG.ch_level:',CONF.LOG.ch_level)
	print('CONF.LOG.fh_level:',CONF.LOG.fh_level)
	print('CONF.REQUEST.http_time:',CONF.REQUEST.http_time)
	print('CONF.REQUEST.retries:',CONF.REQUEST.retries)
	print('CONF.REQUEST.delay:',CONF.REQUEST.delay)
	print('CONF.REQUEST.backoff:',CONF.REQUEST.backoff)
	print('CONF.REQUEST.failonerror:',CONF.REQUEST.failonerror)
