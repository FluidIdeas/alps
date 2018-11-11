#!/usr/bin/env python3

import subprocess

def script_path(script_name, config):
	return config['SCRIPTS_DIR'] + '/' + script_name + '.sh'

def append_unique(lst, item):
	if item not in lst:
		lst.append(item)

def concat_opts(opt_list, default, delim):
	return_value = ''
	for opt in opt_list:
		if default == opt:
			return_value = return_value + opt.upper()
		else:
			return_value = return_value + opt.lower()
		return_value = return_value + delim
	return '(' + return_value[:-1] + ') :'

def graceful_exit():
	print('Exiting...')
	print('')
	exit(0)

def error_exit():
	print('Aborting...')
	print('')
	exit(1)

def list_for_item(item):
	lst = list()
	lst.append(item)
	return lst

def params_and_opts(cmdline_args):
	return_value = (list(), list())
	for arg in cmdline_args:
		if arg.startswith('-'):
			return_value[1].append(arg)
		else:
			return_value[0].append(arg)
	return return_value

def execute_cmd(cmd):
	p = subprocess.Popen(cmd, shell=True)
	p.communicate()
	return_code = p.wait()
	if return_code != 0:
		print('Error occured in the execution of ' + (' ').join(cmd))
		error_exit()

