import pytest
from pyang.statements import ModSubmodStatement, ContainerStatement, \
    LeafLeaflistStatement

from pyangbind.plugin.sqlbind import build_simple_classes


@pytest.fixture
def module():
    statement = ModSubmodStatement(top=None, parent=None, pos=None, keyword='module')
    statement.arg = 'person'
    statement.i_children = []

    return statement


@pytest.fixture
def container(module):
    address_container = ContainerStatement(top=module, parent=module, pos=None, keyword='container')
    address_container.arg = 'address'

    return address_container


def test_should_generate_sqlalchemy_imports(module):

    code = build_simple_classes(None, [module])

    assert 'from sqlalchemy import orm\nimport sqlalchemy as sla' in code


def test_should_generate_class_signature(module):
    code = build_simple_classes(None, [module])

    assert 'class Person:\n' in code


def test_should_generate_orm_relationship(module, container):
    container.i_children = [LeafLeaflistStatement(None, None, None, None)]
    module.i_children = [container]

    code = build_simple_classes(None, [module])

    assert 'address = orm.relationship("Address", back_populates="persons")\n' in code


def test_should_generate_sub_class(module, container):
    container.i_children = [LeafLeaflistStatement(None, None, None, None)]
    module.i_children = [container]

    code = build_simple_classes(None, [module])

    assert 'class Address:\n' in code


def test_should_generate_attributes_for_sub_class(module, container):
    leaf = LeafLeaflistStatement(None, None, None, None)
    leaf.arg = "street"
    container.i_children = [leaf]
    module.i_children = [container]
    code = build_simple_classes(None, [module])

    assert 'street = sla.Column(sla.String)\n' in code
