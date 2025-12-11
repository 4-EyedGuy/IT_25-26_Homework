from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .db_orm import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True, nullable=False)
    is_valid = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")

class Order(Base):
    """Модель заказа с привязкой к пользователю"""
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    goods = relationship("Good", back_populates="order", cascade="all, delete-orphan")

class Good(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    name = Column(String)
    count = Column(Integer)
    price = Column(Float)
    order = relationship("Order", back_populates="goods")
