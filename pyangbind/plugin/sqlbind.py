from __future__ import unicode_literals

import six
from pyang import plugin, statements, util

# Python3 support
if six.PY3:
	long = int
else:
	import codecs

DEBUG = True
if DEBUG:
	import pprint

	pp = pprint.PrettyPrinter(indent=2)


# Base machinery to support operation as a plugin to pyang.
def pyang_plugin_init():
	plugin.register_plugin(PyangBindClass())


class PyangBindClass(plugin.PyangPlugin):

	def add_output_format(self, fmts):
		# Add the 'pybind' output format to pyang.
		self.multiple_modules = True
		fmts["sqlbind"] = self

	def emit(self, ctx, modules, fd):
		# When called, call the build_pyangbind function.
		code = build_simple_classes(ctx, modules)
		write_code_to_file(code, fd)

	def add_opts(self, optparser):
		pass


def build_simple_classes(ctx, modules):
	modules_dict = {}
	for mod in modules:
		modules_dict[mod.arg] = mod

	# list of module names to generate code for
	pyang_called_modules = modules_dict.keys()

	code = ""
	code = generate_imports(code)

	subclasses = []

	for module_name in pyang_called_modules:
		module = modules_dict[module_name]

		code += '\n\n'
		code += generate_class_signature(module_name.capitalize())
		code += generate_table_name(module_name)
		code += generate_primary_key()

		for child in filter_valid_children(module):
			if child.i_children:
				code += generate_orm_relationship(child)
				subclasses.append(child)

		for subclass in subclasses:
			code += "\n\n"
			code += generate_class_signature(subclass.arg.capitalize())
			code += generate_table_name(subclass.arg)
			code += generate_primary_key()

			for child in subclass.i_children:
				code += generate_string_attribute(child)

		code += "\n"
		return code


def generate_primary_key():
	return '    id = sla.Column(sla.Integer, primary_key=True)\n'


def generate_class_signature(class_name):
	return 'class %s(Base):\n' % (class_name)


def generate_table_name(module_name):
	# TODO: Replace with some more advanced logic
	if module_name[-1] == 's':
		module_name = module_name + "e"
	return '    __tablename__ = "%ss"\n' % (module_name)


def generate_string_attribute(child):
	return "\n    %s = sla.Column(sla.String)" % (child.arg)


def generate_orm_relationship(child):
	orm_relation = '\n    address_id = sla.Column(sla.Integer, sla.ForeignKey("addresses.id"))\n'
	orm_relation += '    %s = orm.relationship("%s")\n' % (
		child.arg,
		child.arg.capitalize())
	return orm_relation


def write_code_to_file(code, fd):
	for line in code:
		fd.write(line)


def filter_valid_children(module):
	return [children for children in module.i_children if children.keyword in statements.data_definition_keywords]


def generate_imports(code):
	code += "from desire.db.models import Base\n"
	code += "from sqlalchemy import orm\n"
	code += "import sqlalchemy as sla\n"
	return code
