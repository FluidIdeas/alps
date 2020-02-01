#!/usr/bin/env python3

import subprocess
from controllerthread import ControllerThread

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

def normal_exit():
	print('Exiting...')
	print('')
	exit(0)

def abnormal_exit():
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
	ControllerThread(p).start()
	p.communicate()
	return_code = p.wait()
	if return_code != 0:
		print('Error occured in the execution of ' + (' ').join(cmd))
		abnormal_exit()

def print_help(config):
	print('alps 2.0, The package management tool for AryaLinux.\nRepository version: ' + config['REPO_VERSION'] + '\n' +
'''Usage: alps [flags...] <command> [package]... [source_tarball_path] [source_url]

Flags:
        -ni        --no-interactive        No Interactive. Do not ask for confirmation before performing action
        --help                             Display this help

Commands:
		clear			Clean up the source directory
        help            Print this help message
        install         Install packages alongwith dependencies
        listinstalled   List the packages that are installed with version and date/time of installation
        repoversion     Set the version of repository from where scripts would be downloaded
                        By default the latest version of repository is used
        srcinstall      Try to install the package, given the path to source tarball
        selfupdate      Update alps
		update			Update single package
		updateall		Update all packages that needs update
        updatescripts   Update buildscripts
        urlinstall      Try to install the package, given the URL to the source tarball

Examples:
       alps install rhythmbox vlc
       alps srcinstall /home/foo/baz.tar.bz2
       alps urlinstall http://foo.com/baz.tar.gz
       alps selfupdate
       alps updatescripts
       alps repoversion 2.0
	   alps updateall
	   alps update gedit''')
