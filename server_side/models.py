import secrets

from celery.worker.strategy import default

from database import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, DateTime, BigInteger
from datetime import datetime, UTC
from sqlalchemy.orm import relationship

def generate_token():
    return secrets.token_urlsafe(32)

class User(Base):
    __tablename__ = 'user_detail'

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    phone_number = Column(BigInteger, unique=True, default=None)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)
    register_date = Column(DateTime, default=lambda: datetime.now(UTC))
    customer_associations = relationship("UserCustomer", back_populates="user", cascade="all, delete-orphan")


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_detail.user_id', ondelete='CASCADE'), unique=True)
    active = Column(Boolean, default=True)
    register_date = Column(DateTime, default=lambda: datetime.now(UTC))


class Bakery(Base):
    __tablename__ = 'bakery'

    bakery_id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    token = Column(String, nullable=False, default=generate_token)
    register_date = Column(DateTime, default=lambda: datetime.now(UTC))

    bread_associations = relationship("BakeryBread", back_populates="bakery", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="bakery")


class BreadType(Base):
    __tablename__ = 'bread_type'

    bread_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    register_date = Column(DateTime, default=lambda: datetime.now(UTC))

    bakery_associations = relationship("BakeryBread", back_populates="bread", cascade="all, delete-orphan")
    customer_associations = relationship("CustomerBread", back_populates="bread", cascade="all, delete-orphan")


class BakeryBread(Base):
    __tablename__ = 'bakery_bread'

    bakery_id = Column(Integer, ForeignKey('bakery.bakery_id', ondelete='CASCADE'), primary_key=True)
    bread_type_id = Column(Integer, ForeignKey('bread_type.bread_id', ondelete='CASCADE'), primary_key=True)
    cook_time_s = Column(Integer, nullable=False)

    bakery = relationship("Bakery", back_populates="bread_associations")
    bread = relationship("BreadType", back_populates="bakery_associations")


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hardware_customer_id = Column(Integer, nullable=False)
    bakery_id = Column(Integer, ForeignKey('bakery.bakery_id', ondelete='CASCADE'))
    is_in_queue = Column(Boolean, nullable=False)
    register_date = Column(DateTime, default=lambda: datetime.now(UTC))

    bread_associations = relationship("CustomerBread", back_populates="customer", cascade="all, delete-orphan")
    user_associations = relationship("UserCustomer", back_populates="customer", cascade="all, delete-orphan")
    bakery = relationship("Bakery", back_populates="customers")


class CustomerBread(Base):
    __tablename__ = 'customer_bread'

    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), primary_key=True)
    bread_type_id = Column(Integer, ForeignKey('bread_type.bread_id', ondelete='CASCADE'), primary_key=True)
    count = Column(Integer, nullable=False, default=1)

    customer = relationship("Customer", back_populates="bread_associations")
    bread = relationship("BreadType", back_populates="customer_associations")


class UserCustomer(Base):
    __tablename__ = 'user_customer'

    user_id = Column(Integer, ForeignKey('user_detail.user_id', ondelete='CASCADE'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), primary_key=True)

    user = relationship("User", back_populates="customer_associations")
    customer = relationship("Customer", back_populates="user_associations")
