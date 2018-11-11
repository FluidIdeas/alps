#!/usr/bin/env python3

import sys
sys.path.append('/var/lib/alps')
from misc import script_path
from misc import append_unique
from misc import abnormal_exit

def dependencies(pkg_name, dependency_type, config):
	try:
		with open(pkg_name) as f:
			lines = f.readlines()
		deps = list()
		for line in lines:
			if line != '':
				if line.startswith(dependency_type):
					deps.append(line.strip().replace(dependency_type, ''))
		return deps
	except FileNotFoundError:
		print()
		parts = pkg_name.split('/')
		print('Not able to find buildscript for ' + parts[len(parts) - 1].replace('.sh', ''))
		abnormal_exit()

def required_deps(pkg_name, config):
	return dependencies(script_path(pkg_name, config), '#REQ:', config)

def recommended_deps(pkg_name, config):
	return dependencies(script_path(pkg_name, config), '#REC:', config)

def optional_deps(pkg_name, config):
	return dependencies(script_path(pkg_name, config), '#OPT:', config)

def all_deps(pkg_name, config):
	required = required_deps(pkg_name, config)
	recommended = recommended_deps(pkg_name, config)
	optional = optional_deps(pkg_name, config)
	required.extend(recommended)
	required.extend(optional)
	return required;

def required_and_recommended_deps(pkg_name, config):
	required = required_deps(pkg_name, config)
	recommended = recommended_deps(pkg_name, config)
	required.extend(recommended)
	return required

def dep_chain_individual(pkg_name, processed, include_optional, config):
	if pkg_name in processed:
		return list()
	processed.append(pkg_name)

	if include_optional:
		deps = all_deps(pkg_name, config)
	else:
		deps = required_and_recommended_deps(pkg_name, config)
	dep_chain = list()
	for dep in deps:
		dep_list = dep_chain_individual(dep, processed, include_optional, config)
		for dep_item in dep_list:
			append_unique(dep_chain, dep_item)
	dep_chain.append(pkg_name)
	return dep_chain

def dep_chain(pkg_names, processed, include_optional, config):
	big_dep_chain = list()
	for pkg_name in pkg_names:
		dep_chain = dep_chain_individual(pkg_name, processed, include_optional, config)
		for dep in dep_chain:
			append_unique(big_dep_chain, dep)
	return big_dep_chain

def load_installed(config):
	with open(config['INSTALLED_LIST']) as f:
		lines = f.readlines()
	installed = list()
	for line in lines:
		installed.append(line.split('=')[0])
	return installed

def dep_chain_status(pkg_names, include_optional, config):
	installed = load_installed(config)
	dep_chain_lst = dep_chain(pkg_names, list(), include_optional, config)
	return_list = dict()
	for dep in dep_chain_lst:
		if dep not in installed:
			return_list[dep] = False
		else:
			return_list[dep] = True
	return return_list

