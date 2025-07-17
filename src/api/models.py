from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, CheckConstraint, Date,Boolean,Table,DateTime,func,select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Optional
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=True,default="User")
    stores: Mapped[List["Store"]] = relationship("Store", back_populates="user")
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=1)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
    def serialize_register(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role":self.role,
            # do not serialize the password, its a security breach
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Hashea con pbkdf2:sha256

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Valida el Hash del password
    

store_category_asociation=Table(
    "store_category",
    db.metadata,
    db.Column("store_id",db.Integer,ForeignKey("stores.id"), primary_key = True ),
    db.Column("categories_id",db.Integer,ForeignKey("categories.id"), primary_key = True )
)

class Store(db.Model):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    fecha_de_pago: Mapped[Date] = mapped_column(Date, nullable=True)  
    total_points: Mapped[int] = mapped_column(nullable=True)

    menus = relationship("Menu", back_populates="store")
    user: Mapped["User"] = relationship("User", back_populates="stores")
    categories: Mapped[List["Category"]] = relationship(
        "Category", 
        secondary=store_category_asociation, 
        back_populates="stores"
    )

    # Relación polimórfica a imágenes (solo lectura)
    images = relationship(
        "Image",
        primaryjoin="and_(foreign(Image.owner_id) == Store.id, Image.owner_type == 'store')",
        viewonly=True
    )

    points = relationship("UserPoint", back_populates="store")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.nombre,
            "address": self.direccion,
            "user_id": self.user_id,
            "images": [img.serialize_store() for img in self.images],
            "points": [point.serialize() for point in self.points],
            "total_points":self.total_points,
            "is_active": self.is_active
        }
    def serialize_menu(self):
        return {
            "id": self.id,
            "name": self.nombre
        }
    
class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    stores: Mapped[List[Store]] = relationship("Store", secondary=store_category_asociation, back_populates="categories")


class Menu(db.Model):
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    store = relationship("Store", back_populates="menus")
    products = relationship("Product", back_populates="menu")

    # Relación polimórfica con imágenes
    images = relationship(
        "Image",
        primaryjoin="and_(foreign(Image.owner_id) == Menu.id, Image.owner_type == 'menu')",
        viewonly=True
    )
    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "store": self.store.serialize(),
            "products": [product.serialize_menu() for product in self.products],
            "images": [img.serialize_store() for img in self.images]
        }

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menus.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    menu = relationship("Menu", back_populates="products")

    # Relación polimórfica con imágenes
    images = relationship(
        "Image",
        primaryjoin="and_(foreign(Image.owner_id) == Product.id, Image.owner_type == 'product')",
        viewonly=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "menu_id": self.menu_id,
            "images": [img.serialize() for img in self.images],
            "price": self.price
        }


# consultar con filtro Image.query.filter_by(owner_type='store', owner_id=store.id).all()
class Image(db.Model):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    owner_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'store', 'product', 'user', 'menu'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(default=0, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "url": self.url,
            "position": self.position,
            "owner_type": self.owner_type,
            "owner_id": self.owner_id,
            "user_id": self.user_id
        }
    def serialize_store(self):
        return {
            "url": self.url,
            "position": self.position,
        }

class UserPoint(db.Model):
    __tablename__ = "userpoints"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    points: Mapped[int] = mapped_column(nullable=True)
    store = relationship("Store", back_populates="points")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "store_id": self.store_id,
            "description": self.description,
            "points": self.points,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    

    @classmethod
    def total(cls, store_id, session):
        result = session.execute(
            select(func.avg(cls.points)).where(cls.store_id == store_id)
        ).scalar()
        return result or 0  # Devuelve 0 si no hay resultados
