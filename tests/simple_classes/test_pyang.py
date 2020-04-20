import os
import subprocess
import pytest

GENERATED_CODE_FILE = "binding.py"


@pytest.fixture
def call_pyang():

	def _call_pyang(yang_file):
		# TODO: pyang must be installed!
		pyang_path = 'pyang'
		plugin_dir = '../../pyangbind/plugin'
		pyang_cmd = "{pyang} --plugindir {plugins} -f sqlbind -o {binding} {yang_file}".format(
			pyang=pyang_path,
			plugins=plugin_dir,
			yang_file=yang_file,
			binding=GENERATED_CODE_FILE
		)
		bindings_code = subprocess.check_output(
			pyang_cmd, shell=True, stderr=subprocess.STDOUT, env={}
		)
		exec(bindings_code)

	return _call_pyang


@pytest.fixture
def generate_code(call_pyang):
	yield call_pyang('person.yang')
	os.remove(GENERATED_CODE_FILE)


def test_should_generate_person_class(generate_code):

	from tests.simple_classes.binding import Person

	assert Person() is not None


def test_should_generate_address_attribute(generate_code):

	from tests.simple_classes.binding import Person

	assert_attribute_exists('address', Person())


def test_should_generate_subclass_for_container(generate_code):

	from tests.simple_classes.binding import Address

	assert Address() is not None


def test_should_generate_street_attribute(generate_code):

	from tests.simple_classes.binding import Address

	assert_attribute_exists('street', Address())


def assert_attribute_exists(attribute, person):
	attributes = [attr for attr in dir(person)
	              if not attr.startswith('__')]
	assert attribute in attributes

