import json
import os

import pytest

from tests.simple_classes.test_base import call_pyang

GENERATED_CODE_FILE = "binding_json.py"

@pytest.fixture
def generate_code(call_pyang):
	#yield call_pyang('person.yang', GENERATED_CODE_FILE)
	#os.remove(GENERATED_CODE_FILE)
	pass


def test_json_serialize(generate_code):
	from tests.simple_classes.binding_json import Person, Address
	street = "Lincoln Street"
	address = Address()
	address.street = street
	person = Person()
	person.address = [address]

	# TODO: How to select max_nesting?
	json_str = person.to_json(max_nesting=2)

	assert json_str == '{"address": [{"street": "%s"}]}' % street


def test_json_deserialize(generate_code):
	from tests.simple_classes.binding_json import Person
	street = "Lincoln Street"
	json_str = '{"address": [{"street": "%s"}]}' % street

	person = Person.new_from_json(json_str)

	assert person.address[0].street == street


