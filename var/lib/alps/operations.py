#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')
from misc import script_path
from console import begin_install
import subprocess
from misc import script_path
from misc import graceful_exit
import shlex
import deps
import console
import os

def install_pkg(pkg_name, config):
	try:
		dep_chain = deps.dep_chain_status([pkg_name], False, config)
		console.print_status(dep_chain)
		response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					subprocess.call(shlex.split(script_path(pkg, config)))
	except KeyboardInterrupt:
		graceful_exit()

def install_pkgs(pkg_names, config):
	try:
		dep_chain = deps.dep_chain_status(pkg_names, False, config)
		console.print_status(dep_chain)
		response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					subprocess.call(shlex.split(script_path(pkg, config)))
	except KeyboardInterrupt:
		graceful_exit()

def execute_script(script_path, params):
	try:
		subprocess.call(shlex.split(script_path).extend(params));
	except KeyboardInterrupt:
		graceful_exit()

def update_scripts(config):
	execute_script(config['LIB'] + 'updatescripts.sh', [])

def self_update(config):
	execute_script(config['LIB'] + 'selfupdate.sh', [])

def url_install(url, config):
	execute_script(config['LIB'] + 'urlinstall.sh', [url])

def src_install(tarball_path, config):
	execute_script(config['LIB'] + 'srcinstall.sh', [tarball_path])

def list_installed(config):
	execute_script(config['LIB'] + 'listinstalled.sh', config)

def get_updates(config):
	updateable = list()
	with open(config['VERSION_LIST']) as f:
		installed_versions = f.readlines()
	for installed_version in installed_versions:
		parts = line.split(':')
		script_name = parts[0]
		version = parts[1]
		available_version = script_version(script_name)
		if available_version > version:
			updateable.append(script_name)
	return updateable

def script_version(script_name):
	with open(script_path(script_name, config)) as f:
		for line in f:
			if line.startswith('VERSION='):
				return line[8:].strip()

def load_pkg_versions(config):
	pass

def update(config):
	pass

def run_cmd(cmd, args, config):
	if cmd == 'install':
		if len(args) < 3:
			console.install_not_enough_args_err_msg()
			graceful_exit()
		install_pkgs(args[2:], config)
	elif cmd == 'updatescripts':
		update_scripts(config)
	elif cmd == 'selfupdate':
		self_update(config)

