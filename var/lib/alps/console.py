#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')
from misc import script_path
from misc import concat_opts
from misc import normal_exit
from misc import abnormal_exit

def print_status(status_dict):
	print('')
	installed = list()
	not_installed = list()
	for (pkg, status) in status_dict.items():
		if status == True:
			installed.append(pkg)
		else:
			not_installed.append(pkg)
	if len(not_installed) == 0:
		print('Package(s) already installed.')
		print()
		normal_exit()
	if len(installed) > 0:
		print('The following packages are already installed, not installing again:')
		print('')
		print(', '.join(installed))
		print('')
	if len(not_installed) > 0:
		print('The following packages would be installed:')
		print('')
		print(', '.join(not_installed))

def begin_install(script_name):
	print('')
	print('Executing ' + script_name)
	print('')

def prompt(msg):
	print('')
	return input(msg)

def prompt_choice(msg, options, default):
	try:
		suffix = concat_opts(options, default, '/')
		response = prompt(msg + ' ' + suffix + ' ')
		if response == '':
			return default
		return response
	except KeyboardInterrupt:
		abnormal_exit()

def menu(choices, heading, default):
	try:
		print('')
		print(heading)
		print('')
		count = 1
		opts = list()
		for choice in choices:
			if (default == count):
				print(str(count) + '. ' + choice + ' (default)')
			else:
				print(str(count) + '. ' + choice)
			opts.append(str(count))
			count = count + 1
		print('')
		return prompt_choice('Choose an option', opts, default)
	except KeyboardInterrupt:
		abnormal_exit()

def install_not_enough_args_err_msg():
	print()
	print('Please provide package name for installation. Usage: alps install package name')
	print()

