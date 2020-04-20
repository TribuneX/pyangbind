import subprocess

import pytest


@pytest.fixture
def call_pyang():

	def _call_pyang(yang_file, binding_file):
		# TODO: pyang must be installed!
		pyang_path = 'pyang'
		plugin_dir = '../../pyangbind/plugin'
		pyang_cmd = "{pyang} --plugindir {plugins} -f sqlbind -o {binding} {yang_file}".format(
			pyang=pyang_path,
			plugins=plugin_dir,
			yang_file=yang_file,
			binding=binding_file
		)
		bindings_code = subprocess.check_output(
			pyang_cmd, shell=True, stderr=subprocess.STDOUT, env={}
		)
		exec(bindings_code)

	return _call_pyang
