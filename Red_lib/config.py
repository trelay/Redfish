#!/usr/bin/python3
from oslo.config import cfg

resetful_opts = [
	cfg.StrOpt(
		name='cfg_file',
		default=None,
		help='Path of this very file'),

	cfg.StrOpt(
		name='value_file',
		default=None,
		help='Path of comparing file'),

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
		help='The ver of Redfish this app supports.'),

	cfg.IntOpt(
		name='cycle',
		default=2,
		help='cycle to execute.'),
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
	#default='./redfish.log',
	default=None,
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
	name='cycle',
	default= 3,
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
CONF.register_opts(resetful_opts)

CONF.register_group(log_group)
CONF.register_opts(log_cfg_opts, log_group)

CONF.register_group(request_group)
CONF.register_opts(req_fail_opts, request_group)

if __name__ =="__main__":
	CONF(default_config_files=['Redfish.conf'])
	print(CONF.cfg_file)
	print(CONF.client_name)
	print(CONF.bind_port)
	print(CONF.ver_support)
	print(CONF.LOG.app_name)
	print(CONF.LOG.logfilename)
	print(CONF.LOG.log_format)
	print(CONF.LOG.root_level)
	print(CONF.LOG.ch_level)
	print(CONF.LOG.fh_level)
	print(CONF.REQUEST.http_time)
	print(CONF.REQUEST.cycle)
	print(CONF.REQUEST.delay)
	print(CONF.REQUEST.backoff)
	print(CONF.REQUEST.failonerror)
