from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, ForeignKey, Boolean, Float, select, func, alias, \
    join, outerjoin, and_
import enum
from items_control.data import db
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship, column_property
# from items_control.orm.base import Base
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from items_control.data import db
from sqlalchemy.sql import text

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



#------------------PROCEDENCIA----------------------------------

class Procedencia(Base):
    __tablename__ = "procedencia"

    id = Column(Integer,primary_key=True)
    nombre = Column(String(50))
    fecha = Column(Date)
    detalle = Column(String(200))

    #relacion con items
    item = relationship('Item', backref="procedencia")

    def __repr__(self):
        return "Procedencia<-%s-,'%s'>" % (self.id,self.nombre)

#----------------------ITEM------------------------------------------

class ItemPadre(Base):
    __tablename__ = "item_padre"

    id = Column(Integer,primary_key=True)
    nombre = Column(String(50))
    marca  = Column(String(50))
    foto = image_attachment('ItemPhoto')
    items = relationship('Item', backref="parent")

    def __repr__(self):
        return "ItemPadre<-%s-,'%s','%s'>" % (self.id,self.nombre,self.marca)

class ItemPhoto(Base, Image):
    """Fotos de los Items"""
    __tablename__ = 'item_photo'

    item_id = Column(Integer,ForeignKey('item_padre.id'), primary_key=True)
    item = relationship('ItemPadre')

    def __repr__(self):
        return "ItemPhoto<-%s->" % (self.id)


# --------------------------------Ventas--------------------------------------------------------
class Venta(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    cantidad = Column(DateTime)
    precio = Column(Integer)
    invalidada = Column(Boolean)
    observaciones = Column(String)

    # cliente
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente', backref="ventas")

    # items
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', backref="venta")

    def __repr__(self):
        return "Venta<-%s-,'%s',%s,%s>" % (self.id, self.fecha, self.cantidad, self.precio)


# -----------------------------Item Movido-----------------------------------------------

class ItemMovido(Base):
    __tablename__ = "items_movido"

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    observaciones = Column(String(200))

    # movimiento
    movimiento_id = Column(Integer, ForeignKey('movimiento.id'))

    # item
    item_id = Column(Integer, ForeignKey('item.id'))

    # item = relationship('Item')

    def __repr__(self):
        return "ItemMovido<-%s-,'%s'>" % (self.id, self.cantidad)


# ------------------------------MOVIMIENTO------------------------------------------------
class TipoMovimiento(enum.Enum):
    SALIDA = 1
    DEVOLUCION = 2


class Movimiento(Base):
    """Maneja los movimientos de ropa"""

    def __init__(self, fecha=datetime.now()):
        Base.__init__(self)
        self.fecha = fecha

    __tablename__ = "movimiento"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    tipo = Column(Enum(TipoMovimiento))

    items = relationship('ItemMovido', backref="movimiento")

    # cliente link
    cliente_id = Column(Integer, ForeignKey("cliente.id"))

    def __repr__(self):
        return "Movimiento<-%s-,'%s','%s'>" % (self.id, self.fecha, self.tipo)


class Item(Base):
    """Store Item info"""

    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    costo = Column(Float)
    
    #parent
    parent_id = Column(Integer,ForeignKey('item_padre.id'))

    #procedencia
    procedencia_id = Column(Integer,ForeignKey('procedencia.id'))

    #precio
    precio = relationship('PrecioVenta', backref='item')

    #movimientos
    movimientos = relationship('ItemMovido', backref="item")

    # select *, (cantidad - ifnull(salidas,0) + ifnull(entradas,0)) as resultante from item left join
    # (select im.item_id as id1, ifnull(sum(cantidad),0) as salidas from items_movido as im
    # left join movimiento as m on m.id = im.movimiento_id where m.tipo == 'SALIDA' group by im.item_id)
    # as r1 on item.id = r1.id1 left join
    # (select im.item_id as id2, ifnull(sum(cantidad),0) as entradas from items_movido as im left join
    # movimiento as m on m.id = im.movimiento_id where m.tipo == 'DEVOLUCION' group by im.item_id) as r2 on r1.id1 = r2.id2

    # salidas = alias(func.sum(ItemMovido.cantidad))
    # entradas = alias(func.sum(ItemMovido.cantidad))

    salidas = column_property(select([func.ifnull(func.sum(ItemMovido.cantidad), 0)]).
                              where(and_(Movimiento.tipo == TipoMovimiento.SALIDA,
                                         ItemMovido.item_id == id,
                                         ItemMovido.movimiento_id == Movimiento.id)))

    devoluciones = column_property(select([func.ifnull(func.sum(ItemMovido.cantidad), 0)]).
                                   where(and_(Movimiento.tipo == TipoMovimiento.DEVOLUCION,
                                              ItemMovido.item_id == id,
                                              ItemMovido.movimiento_id == Movimiento.id)))

    vendidos = column_property(select([func.ifnull(func.sum(Venta.cantidad), 0)]).
                               where(and_(Venta.item_id == id,
                                          Venta.invalidada is False)))

    restantes = column_property(cantidad - salidas + devoluciones - vendidos)

    # outerjoin(ItemMovido, ItemMovido.item_id == id).
    # outerjoin(Movimiento, ItemMovido.movimiento_id == Movimiento.id).label('salidas')
    # )

    # r_salida = alias(select([ItemMovido, func.sum(ItemMovido.cantidad).label('salidas')]).
    #                  where(Movimiento.tipo == TipoMovimiento.SALIDA).group_by(ItemMovido.id).
    #                  outerjoin(Movimiento, Movimiento.id == ItemMovido.movimiento_id))
    #
    # r_devolucion = alias(select([ItemMovido, func.sum(ItemMovido.cantidad).label('entradas')]).
    #                      where(Movimiento.tipo == TipoMovimiento.DEVOLUCION).group_by(ItemMovido.id).
    #                      outerjoin(Movimiento, Movimiento.id == ItemMovido.movimiento_id))
    #
    #
    # #atributos para saber los restantes
    # restantes = column_property(select([cantidad]).
    #     outerjoin(r_salida, id == r_salida.c.item_id).
    #     outerjoin(r_devolucion, id == r_devolucion.c.item_id))

    def addPrecio(self, precio):
        """
        Agrega un precio a los items, actualiza las fecha de inicio y fin de los precios anteriores
        :param precio:
        :return:
        """

        if isinstance(precio, float) or isinstance(precio, int):
            precio = PrecioVenta.newPrecio(precio)

        if isinstance(precio, PrecioVenta):
            if len(self.precio) > 0:
                last = self.precio[-1]
                last.fecha_fin = datetime.now()
            self.precio.append(precio)

    def __repr__(self):
        return "Item<-%s-,'%s'>" % (self.id,self.cantidad)
    
class PrecioVenta(Base):
    __tablename__ = "precio_venta"

    id = Column(Integer, primary_key=True)
    precio = Column(Float)
    fecha_inicio = Column(Date)
    fecha_final = Column(Date)

    item_id = Column(Integer, ForeignKey('item.id'))
    # item = relationship('Item',back_populates='precio')

    @staticmethod
    def newPrecio(precio, fecha_inicio=None):
        p = PrecioVenta()
        p.precio = precio
        if fecha_inicio is None:
            fecha_inicio = datetime.now()
        p.fecha_inicio = fecha_inicio
        return p

    def __repr__(self):
        return "PrecioVenta<-%s-,'%s','%s'>" %(self.id,self.fecha_inicio,self.fecha_final)


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    telefono = Column(String(50))
    direccion = Column(String(300))
    tipo = Column(Enum(TipoClienteEnum))

    # movimientos

    movimientos = relationship("Movimiento", backref="cliente")

    @hybrid_method
    def posession_items(self):
        # TODO: Make this from another way. This is for going fast and is a shit

        engine = db.Engine.instance
        with engine.connect() as conn:
            sql = """ select r1.item_id, (ifnull(r1.total_sal,0) - ifnull(r2.total_dev,0)) as tiene
            from (select im.item_id, m.tipo, c.nombre, sum(im.cantidad) as total_sal, m.cliente_id from movimiento as m 
            left join items_movido as im on im.movimiento_id == m.id left join cliente as c on c.id == m.cliente_id
            where m.tipo = "SALIDA" and c.id == %d group by im.item_id, m.tipo,m.cliente_id) as r1
            left join (select im.item_id, m.tipo, c.nombre, sum(im.cantidad)as total_dev, m.cliente_id  from movimiento as m
            left join items_movido as im on im.movimiento_id == m.id left join cliente as c on c.id == m.cliente_id 
            where m.tipo = "DEVOLUCION" group by im.item_id, m.tipo) as r2 on r1.item_id == r2.item_id and r1.cliente_id == r2.cliente_id 
            left join item on item.id == r1.item_id;
                    """ % self.id

            results = conn.execute(text(sql))
            r = []
            ids = []
            for row in results:
                ids.append(row['item_id'])
                r.append((row['item_id'], row['tiene']))
                # i = Item()
                # i.id = row['id']
                # i.cantidad = row['cantidad']
                # i.procedencia_id = row['procedencia_id']
                # i.parent_id = row['parent_id']
                # i.costo = row['costo']
                # i.tiene = row['tiene']
                # items.append(i)

            session = db.session()
            items = session.query(Item).filter(Item.id.in_(ids)).all()
            for i in items:
                for row in r:
                    if row[0] == i.id:
                        i.tiene = row[1]
                        break

            return items

        # rs = select([ItemMovido, func.sum(ItemMovido.cantidad)]). \
        #             where(and_(Movimiento.tipo == TipoMovimiento.SALIDA)).\
        #             group_by(ItemMovido.item_id, Movimiento.cliente_id)


    # select r1.item_id, r1.nombre, r1.cliente_id, r1.total_sal, r2.total_dev, (
    #             ifnull(r1.total_sal, 0) - ifnull(r2.total_dev, 0)) as tiene
    # from (select im.item_id, m.tipo, c.nombre, sum(im.cantidad) as total_sal, m.cliente_id
    # from movimiento as m
    # left join items_movido as im on  im.movimiento_id == m.id
    # left join cliente as c on c.id == m.cliente_id
    # where m.tipo = "SALIDA" group by im.item_id, m.tipo, m.cliente_id) as r1
    # left join (select im.item_id, m.tipo, c.nombre, sum(im.cantidad)as total_dev, m.cliente_id
    # from movimiento as m
    # left join items_movido as im on im.movimiento_id == m.id
    # left join cliente as c on c.id == m.cliente_id
    # where m.tipo = "DEVOLUCION"
    # group by im.item_id, m.tipo) as r2 on r1.item_id == r2.item_id and r1.cliente_id == r2.cliente_id

    # @staticmethod
    # def create_table():
    #     Base.metadata.create_all(engine)

    def __repr__(self):
        return "Cliente<-%s-,'%s','%s'>" % (self.id, self.nombre, self.tipo)
