from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .database import Base

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String)

    products = relationship(
        "Product",
        back_populates="type"
    )

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact = Column(String)
    email = Column(String)
    phone = Column(String)

    products = relationship(
        "Product",
        back_populates="supplier"
    )

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    sku = Column(String(50), unique=True)

    stock = Column(Integer, default=0)
    min_stock = Column(Integer, default=0)

    price = Column(Float, default=0)

    type_id = Column(
        Integer,
        ForeignKey("types.id"),
        nullable=False
    )

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=False
    )

    type = relationship(
        "Type",
        back_populates="products"
    )

    supplier = relationship(
        "Supplier",
        back_populates="products"
    )
