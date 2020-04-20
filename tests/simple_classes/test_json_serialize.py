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


def test_json_deserialize(generate_code):
	from tests.simple_classes.binding_json import Person, Address
	street = "Lincoln Street"

	json_str = '{"address": [{"street": "%s"}]}' % street
	#json_value = json.loads(json_str)

	address = Address()
	address.street = street
	person = Person()
	person.address = [address]

	# json_str = person.to_json(max_nesting=1)
	# print(json_str)


	#person = Person(**json_value)

	# person = Person.new_from_json(json_str)
	#
	# assert person.address[0].street == street


