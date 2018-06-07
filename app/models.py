from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, autoincrement=True, primary_key=True)
    project_id = Column('project', Integer, ForeignKey('project.id'))
    description = Column('description', String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column('login', String, unique=True, nullable=True)
    password_hash = Column('password', String, nullable=True)
    projects = relationship('Project')


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column('user', Integer, ForeignKey('user.id'))
    create_date = Column('date', Date, nullable=True)
    invoices = relationship('Invoice')
