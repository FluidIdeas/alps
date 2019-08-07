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
	p.communicate()
	return_code = p.wait()
	if return_code != 0:
		print('Error occured in the execution of ' + (' ').join(cmd))
		abnormal_exit()

def read_versions(config):
	version_list_path = config['VERSION_LIST']
	with open(version_list_path) as fp:
		lines = fp.readlines()
	versions = dict()
	for line in lines:
		parts = line.split(':')
		versions[parts[0]] = parts[1]
	return versions

def get_installed_version(config, package_name):
	versions = read_versions(config)
	if package_name in versions:
		return versions[package_name]
	else:
		return None

def get_available_version(config, package_name):
	

def print_help(config):
	print('alps 2.0, The package management tool for AryaLinux.\nRepository version: ' + config['REPO_VERSION'] + '\n' +
'''Usage: alps [flags...] <command> [package]... [source_tarball_path] [source_url]

Flags:
        -ni        --no-interactive        No Interactive. Do not ask for confirmation before performing action
        --help                             Display this help

Commands:
        help            Print this help message
        install         Install packages alongwith dependencies
        srcinstall      Try to install the package, given the path to source tarball
        urlinstall      Try to install the package, given the URL to the source tarball
        selfupdate      Update alps
        updatescripts   Update buildscripts
        listinstalled   List the packages that are installed with version and date/time of installation
        repoversion     Set the version of repository from where scripts would be downloaded
                        By default the latest version of repository is used

Examples:
       alps install rhythmbox vlc
       alps srcinstall /home/foo/baz.tar.bz2
       alps urlinstall http://foo.com/baz.tar.gz
       alps selfupdate
       alps updatescripts
       alps repoversion 2.0''')
