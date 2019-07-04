from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, ForeignKey, Boolean
import enum
from items_control.data.db import engine
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship
# from items_control.orm.base import Base

Base = declarative_base()

#-------------USUARIO----------------------------------

class Usuario(Base):
    __tablename__= 'users'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    login = Column(String(50))
    password = Column(String(200))


    def __repr__(self):
        return "Usuario<-%s-,'%s','%s'>" %(self.id,self.login,self.nombre)
#---------------CLIENTE--------------------------------------------------------------------------

class TipoClienteEnum(enum.Enum):
    MAYORITARIO = 1
    MINORITARIO = 2

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    telefono = Column(String(50))
    direccion = Column(String(300))
    tipo = Column(Enum(TipoClienteEnum))

    #movimientos

    movimientos = relationship("Movimiento", backref="cliente")
    
    # @staticmethod
    # def create_table():
    #     Base.metadata.create_all(engine)

    def __repr__(self):
        return "Cliente<-%s-,'%s','%s'>" %(self.id,self.nombre,self.tipo)

#------------------PROCEDENCIA----------------------------------

class Procedencia(Base):
    __tablename__ = "procedencia"

    id = Column(Integer,primary_key=True)
    nombre = Column(String(50))
    fecha = Column(Date)
    detalle = Column(String(200))

    #relacion con items
    item = relationship('Item',backref="procedencia")

    def __repr__(self):
        return "Procedencia<-%s-,'%s'>" % (self.id,self.nombre)

#----------------------ITEM------------------------------------------

class ItemPadre(Base):
    __tablename__ = "item_padre"

    id = Column(Integer,primary_key=True)
    nombre = Column(String(50))
    marca  = Column(String(50))
    foto = image_attachment('ItemPhoto')
    items = relationship('Item',backref="parent")

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

    def __repr__(self):
        return "ItemPadre<-%s-,'%s','%s'>" % (self.id,self.nombre,self.marca)

class ItemPhoto(Base, Image):
    """Fotos de los Items"""
    __tablename__ = 'item_photo'

    item_id = Column(Integer,ForeignKey('item_padre.id'), primary_key=True)
    item = relationship('ItemPadre')

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

    def __repr__(self):
        return "ItemPhoto<-%s->" % (self.id)

class Item(Base):
    """Store Item info"""

    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    
    #parent
    parent_id = Column(Integer,ForeignKey('item_padre.id'))
    # parent = relationship('ItemPadre',back_populates="items")

    #procedencia
    procedencia_id = Column(Integer,ForeignKey('procedencia.id'))
    # procedencia = relationship('Procedencia',back_populates="items")

    #precio
    precio = relationship('PrecioVenta',backref='item')

    #movimientos
    movimientos = relationship('ItemMovido',backref="item")

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

    def __repr__(self):
        return "Item<-%s-,'%s'>" % (self.id,self.cantidad)
    
class PrecioVenta(Base):
    __tablename__ = "precio_venta"

    id = Column(Integer, primary_key=True)
    fecha_inicio = Column(Date)
    fecha_final = Column(Date)

    item_id = Column(Integer, ForeignKey('item.id'))
    # item = relationship('Item',back_populates='precio')

    def __repr__(self):
        return "PrecioVenta<-%s-,'%s','%s'>" %(self.id,self.fecha_inicio,self.fecha_final)


#------------------------------MOVIMIENTO------------------------------------------------
class TipoMovimiento(enum.Enum):
    SALIDA = 1
    DEVOLUCION = 2

class Movimiento(Base):
    """Maneja los movimientos de ropa"""

    __tablename__ = "movimiento"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    tipo = Column(Enum(TipoMovimiento))

    items = relationship('ItemMovido', backref="movimiento")

    #cliente link
    cliente_id = Column(Integer, ForeignKey("cliente.id"))
    
    def __repr__(self):
        return "Movimiento<-%s-,'%s','%s'>" %(self.id,self.fecha,self.tipo)
#-----------------------------Item Movido-----------------------------------------------

class ItemMovido(Base):
    __tablename__ = "items_movido"

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    observaciones = Column(String(200))

    #movimiento
    movimiento_id = Column(Integer,ForeignKey('movimiento.id'))
    # movimiento = relationship('Movimiento', back_populates="items")

    #item
    item_id = Column(Integer, ForeignKey('item.id'))
    # item = relationship('Item')

    def __repr__(self):
        return "ItemMovido<-%s-,'%s','%s'>" %(self.id,self.cantidad)

#--------------------------------Ventas--------------------------------------------------------
class Venta(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    cantidad = Column(DateTime)
    precio = Column(Integer)
    invalidada = Column(Boolean)
    observaciones = Column(String)

    #cliente
    cliente_id =Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente',backref="venta")

    #items
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item',backref="venta")

