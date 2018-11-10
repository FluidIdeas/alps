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

