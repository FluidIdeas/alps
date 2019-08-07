#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')

def load_config(config_filename):
	with open(config_filename) as f:
		lines = f.readlines()
	config = dict()
	for line in lines:
		parts = line.split('=')
		config[parts[0].strip()] = parts[1].strip()
	return config

def dump_config(config, config_filename):
	try:
		with open(config_filename, 'w') as f:
			for key, value in config.items():
				f.write(key + '=' + value + '\n')
	except PermissionError:
		print('To change repoversion, please run as sudo. Example: sudo alps repoversion <version>')

