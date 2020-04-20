import os
import pytest
from desire.db.models import Base
from tests.simple_classes.test_base import call_pyang

GENERATED_CODE_FILE = "binding.py"


@pytest.fixture
def generate_code(call_pyang):
	yield call_pyang('person.yang', GENERATED_CODE_FILE)
	# os.remove(GENERATED_CODE_FILE)


def test_should_generate_person_class(generate_code):
	from tests.simple_classes.binding import Person

	assert Person() is not None


def test_should_add_sqlalchemy_base_class(generate_code):
	from tests.simple_classes.binding import Person

	assert isinstance(Person(), Base)


def test_should_generate_address_attribute(generate_code):
	from tests.simple_classes.binding import Person

	assert_attribute_exists('address', Person())


def test_should_generate_subclass_for_container(generate_code):
	from tests.simple_classes.binding import Address

	assert Address() is not None


def test_should_generate_street_attribute(generate_code):
	from tests.simple_classes.binding import Address

	assert_attribute_exists('street', Address())


def test_orm_relationship(generate_code):
	verify_string_exists(
		'orm.relationship("Address", back_populates="persons")')


def test_sla_string_column(generate_code):
	verify_string_exists('street = sla.Column(sla.String)')


def verify_string_exists(string):
	assert open(GENERATED_CODE_FILE, "r").read().find(string)


def assert_attribute_exists(attribute, person):
	attributes = [attr for attr in dir(person)
	              if not attr.startswith('__')]
	assert attribute in attributes

