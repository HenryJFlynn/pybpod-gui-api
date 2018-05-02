import json

SETTINGS_PRIORITY = 0

SERIAL_PORT       = '{serialport}'
NET_PORT          = {netport}

{bnp_ports}
{wired_ports}
{behavior_ports}

PYBPOD_API_LOG_LEVEL = None
PYBPOD_API_LOG_FILE  = None

PYBPOD_API_STREAM2STDOUT = {stream2stdout}
PYBPOD_API_ACCEPT_STDIN  = True

PYBPOD_CREATOR 		= ''
PYBPOD_PROJECT 		= '{project}'
PYBPOD_EXPERIMENT 	= '{experiment}'
PYBPOD_BOARD 		= '{board}'
PYBPOD_SETUP 		= '{setup}'
PYBPOD_SESSION 		= '{session}'
PYBPOD_SESSION_PATH = '{session_path}'
PYBPOD_SUBJECTS 	= json.dump([{subjects}])

#import logging
#PYBPOD_API_LOG_LEVEL = logging.DEBUG
#PYBPOD_API_LOG_FILE  = 'pybpod-api.log'

PYBPOD_VARSNAMES = [{variables_names}]