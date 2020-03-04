#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')
from misc import script_path
from console import begin_install
import subprocess
from misc import script_path
from misc import abnormal_exit
from misc import execute_cmd
import shlex
import deps
import console
import os
import misc
import json
from config import dump_config

config_path = '/etc/alps/alps.conf'

def install_pkg(pkg_name, config):
	try:
		dep_chain = deps.dep_chain_status(misc.list_for_item(pkg_name), False, config)
		console.print_status(dep_chain)
		if not ('-ni' in opts or '--no-interactive' in opts):
			response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		else:
			response = 'y'
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					execute_cmd(script_path(pkg, config).split())
	except KeyboardInterrupt:
		abnormal_exit()

def install_pkgs(pkg_names, opts, config):
	try:
		dep_chain = deps.dep_chain_status(pkg_names, False, config)
		console.print_status(dep_chain)
		if not ('-ni' in opts or '--no-interactive' in opts):
			response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		else:
			response = 'y'
		if response == 'y':
			for (pkg, status) in dep_chain.items():
				if not status:
					begin_install(script_path(pkg, config))
					execute_cmd(script_path(pkg, config).split())
	except KeyboardInterrupt:
		abnormal_exit()

def execute_script(script_path, params=None):
	try:
		if params != None:
			execute_cmd(script_path.split().extend(params))
		else:
			execute_cmd(script_path.split())
	except KeyboardInterrupt:
		abnormal_exit()

def update_scripts(config):
	execute_script(config['LIB'] + 'updatescripts.sh')
	generate_package_list()

def self_update(config):
	execute_script(config['LIB'] + 'selfupdate.sh')

def url_install(url, config):
	params = list()
	params.append
	execute_script(config['LIB'] + 'urlinstall.sh', misc.list_for_item(url))

def src_install(tarball_path, config):
	execute_script(config['LIB'] + 'srcinstall.sh', misc.list_for_item(tarball_path))

def list_installed(config):
	print()
	heading = '%-30s%-15s%-30s' % ('Package Name', 'Version', 'Installation Date')
	print(heading)
	pkgs = load_installed_pkgs(config)
	pkg_versions = load_installed_versions(config)
	pkg_names = list()
	for (name, date) in pkgs.items():
		try:
			# pkg_names.append(name + ' (' + date + ', ' + pkg_versions[name] + ') ')
			line = '%-30s%-15s%-30s' % (name, pkg_versions[name], date)
			pkg_names.append(line)
		except KeyError:
			pass
	print()
	print('\n'.join(pkg_names))
	print()

def sort_updates(config, updateable):
	dep_list = list()
	for p in updateable:
		dep_list.extend(deps.all_deps(p, config))
	final_list = list()
	for dep in dep_list:
		if dep not in final_list and dep in updateable:
			final_list.append(dep)
	return final_list

def get_updates(config):
	updateable = list()
	with open(config['VERSION_LIST']) as f:
		installed_versions = f.readlines()
	for installed_version in installed_versions:
		parts = installed_version.split(':')
		script_name = parts[0]
		version = parts[1].strip()
		available_version = script_version(script_name, config)
		if available_version == None:
			continue
		if available_version > version or version == 'current':
			updateable.append(script_name)
	return sort_updates(config, updateable)

def script_version(script_name, config):
	if not os.path.exists(script_path(script_name, config)):
		return None
	with open(script_path(script_name, config)) as f:
		for line in f:
			if line.startswith('VERSION='):
				return line[8:].strip()

def load_installed_versions(config):
	with open(config['VERSION_LIST']) as f:
		lines = f.readlines()
	versions = dict()
	for line in lines:
		parts = line.split(':')
		try:
			versions[parts[0]] = parts[1].strip()
		except KeyError:
			pass
	return versions

def load_installed_pkgs(config):
	with open(config['INSTALLED_LIST']) as f:
		lines = f.readlines()
	pkgs = dict()
	for line in lines:
		parts = line.split('=')
		try:
			pkgs[parts[0]] = parts[1][1:].strip()
		except KeyError:
			pass
	return pkgs

def update(config):
	pass

def generate_package_list():
	print('Generating package.json...')
	package_installed_dates_and_versions = load_installed_date_and_version()
	packages_list_file = '/var/cache/alps/packages.json'
	packages = list()

	scripts_dir = '/var/cache/alps/scripts'
	scripts = os.listdir(scripts_dir)
	for script in scripts:
		with open(scripts_dir + '/' + script) as fp:
			package = parse_package(fp)
			if 'name' in package and package['name'] in package_installed_dates_and_versions:
				package['version'] = package_installed_dates_and_versions[package['name']]['installed_version']
				package['installed_date'] = package_installed_dates_and_versions[package['name']]['installed_date']
				package['status'] = package_installed_dates_and_versions[package['name']]['status']
		packages.append(package)
	with open('/tmp/pkgs.json', 'w') as fp:
		fp.write(json.dumps(packages, sort_keys=True, indent=4, separators=(',', ': ')))
	process = subprocess.Popen(('sudo cp /tmp/pkgs.json ' + packages_list_file).split())
	process.communicate()

def load_installed_date_and_version():
	with open('/etc/alps/installed-list', 'r') as fp:
		installed_list = fp.read().splitlines()
	with open('/etc/alps/versions', 'r') as fp:
		installed_versions = fp.read().splitlines()
	installed_packages = dict()
	installed_package_versions = dict()
	packages = dict()
	for installed_package in installed_list:
		name = installed_package[0:installed_package.index('=>')]
		date = installed_package[installed_package.index('=>') + 2:]
		installed_packages[name] = date
	for package_version in installed_versions:
		name = package_version[0:package_version.index(':')]
		version = package_version[package_version.index(':') + 1:]
		installed_package_versions[name] = version
	for name in installed_packages.keys():
		version = None
		date = None
		status = False
		if name in installed_packages:
			date = installed_packages[name]
			status = True
			if name in installed_package_versions:
				version = installed_package_versions[name]
		packages[name] = {'installed_date': date, 'installed_version': version, 'status': status}
	return packages

def parse_package(package_file):
	package = dict()
	lines = package_file.read().splitlines()
	for line in lines:
		if 'NAME=' in line and line.index('NAME=') == 0:
			package['name'] = line.replace('NAME=', '').replace('"', '')
		elif 'VERSION=' in line and line.index('VERSION=') == 0:
			package['available_version'] = line.replace('VERSION=', '').replace('"', '')
		elif 'DESCRIPTION=' in line and line.index('DESCRIPTION=') == 0:
			package['description'] = line.replace('DESCRIPTION=', '').replace('"', '')
		if 'name' in package and 'available_version' in package and 'description' in package:
			break
	package['script'] = package_file.name
	package['status'] = False
	return package

def src_install(config, paths):
	for path in paths:
		process = subprocess.Popen(config['LIB'] + 'srcinstall.sh ' + path, shell=True)
		process.communicate()
		process.wait()

def url_install(config, urls):
	for url in urls:
		process = subprocess.Popen(config['LIB'] + 'urlinstall.sh ' + url, shell=True)
		process.communicate()
		process.wait()

def remove_duplicate_entries(config):
	with open(config['INSTALLED_LIST']) as fp:
		installed_lines = fp.readlines()
	installed = dict()
	for line in installed_lines:
		parts = line.split('=')
		installed[parts[0]] = parts[1][1:].strip()
	with open('/tmp/installed-list', 'w') as fp:
		for name, time in installed.items():
			fp.write(name + '=>' + time + '\n')
	with open(config['VERSION_LIST']) as fp:
		version_lines = fp.readlines()
	versions = dict()
	for line in version_lines:
		parts = line.split(':')
		versions[parts[0]] = parts[1].strip()
	with open('/tmp/versions', 'w') as fp:
		for name, time in versions.items():
			fp.write(name + ':' + time + '\n')
	overwrite_package_lists(config)

def overwrite_package_lists(config):
	process = subprocess.Popen(config['LIB'] + 'overwrite_package_lists.sh', shell=True)
	process.communicate()
	process.wait()

def update(config, packages):
	# To update check what is the installed version
	# And what is the available version
	# If they do not match then do installation.
	try:
		to_be_updated = get_updates(config)
		#try:
		#	with open(config['PACKAGE_LIST']) as fp:
		#		package_list = json.loads(fp.read())
		#except:
		#	print('Please run: alps updatescripts before running an update.')
		#	abnormal_exit()
		#to_be_updated = list()
		#for pkg in package_list:
		#	if pkg['name'] in packages and pkg['status'] == True and not pkg['available_version'] == pkg['version']:
		#		to_be_updated.append(pkg['name'])
		#
		update_list = list()
		for package in packages:
			if package in to_be_updated:
				update_list.append(package)
		if len(update_list) == 0:
			print('Latest version already installed. Not updating.')
			abnormal_exit()
		print('The following packages would be updated:\n\t' + ' '.join(update_list))
		response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		if response == 'y':
			for pkg in update_list:
				begin_install(script_path(pkg, config))
				execute_cmd(script_path(pkg, config).split())
				remove_duplicate_entries(config)
	except KeyboardInterrupt:
		abnormal_exit()

def update_all(config):
	# To update check what is the installed version
	# And what is the available version
	# If they do not match then do installation.
	try:
		#try:
		#	with open(config['PACKAGE_LIST']) as fp:
		#		package_list = json.loads(fp.read())
		#except:
		#	print('Please run: alps updatescripts before running an update.')
		#	abnormal_exit()
		to_be_updated = get_updates(config)
		#for pkg in package_list:
		#		if pkg['status'] == True and not pkg['available_version'] == pkg['version']:
		#			to_be_updated.append(pkg['name'])

		print('The following packages would be updated:\n\t' + ' '.join(to_be_updated))
		response = console.prompt_choice('Are you sure you want to install these packages?', ['y', 'n'], 'y')
		if response == 'y':
			for pkg in to_be_updated:
				begin_install(script_path(pkg, config))
				execute_cmd(script_path(pkg, config).split())
				remove_duplicate_entries(config)
	except KeyboardInterrupt:
		abnormal_exit()

def set_repo_version(config, version):
	config['REPO_VERSION'] = version
	dump_config(config, config_path)

def print_repo_version(config):
	print(config['REPO_VERSION'])

def clear(config):
	process = subprocess.Popen(config['LIB'] + 'clear.sh', shell=True)
	process.communicate()
	process.wait()

def run_cmd(cmd, params_and_opts, config):
	if cmd == 'install':
		if len(params_and_opts[0]) < 3:
			console.install_not_enough_args_err_msg()
			abnormal_exit()
		install_pkgs(params_and_opts[0][2:], params_and_opts[1], config)
	elif cmd == 'updatescripts':
		update_scripts(config)
	elif cmd == 'selfupdate':
		self_update(config)
	elif cmd == 'listinstalled':
		list_installed(config)
	elif cmd == 'urlinstall':
		url_install(config, params_and_opts[0][2:])
	elif cmd == 'srcinstall':
		src_install(config, params_and_opts[0][2:])
	elif cmd == 'update':
		update(config, params_and_opts[0][2:])
	elif cmd == 'updateall':
		update_all(config)
	elif cmd == 'clear':
		clear(config)
	elif cmd == 'repoversion':
		if len(params_and_opts[0]) <= 2:
			print_repo_version(config)
		else:
			set_repo_version(config, params_and_opts[0][2])
	elif cmd == 'help':
		misc.print_help(config)
	else:
		print('Unrecognized command: ' + cmd)
		misc.print_help(config)

