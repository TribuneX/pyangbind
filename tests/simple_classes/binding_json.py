#from desire.db.models import ModelBase
#from sqlalchemy import orm
import sqlalchemy as sla

from sqlathanor import declarative_base, Column, relationship


Base = declarative_base()
#Base = declarative_base(cls=ModelBase)

class Person(Base):
    __tablename__ = "persons"
    id = Column(sla.Integer, primary_key=True)

    address = relationship("Address", supports_json=True, supports_dict=True)
    #address = orm.relationship("Address", backref = "person")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(sla.Integer, primary_key=True)

    person_id = Column(sla.Integer, sla.ForeignKey("persons.id"))
    street = Column(sla.String, supports_json=True)
