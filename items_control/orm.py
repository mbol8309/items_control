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
    cantidad = Column(Integer)
    precio = Column(Float)
    invalidada = Column(Boolean)
    observaciones = Column(String)

    # cliente
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente', backref="ventas")

    # items
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', backref="venta")

    def __init__(self, fecha=datetime.now()):
        Base.__init__(self)
        self.fecha = fecha
        self.invalidada = False

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

    @hybrid_method
    def getTracker(self):
        engine = db.Engine.instance
        with engine.connect() as conn:
            sql = """
            select im.item_id, cantidad, m.tipo, m.fecha, "MOVIMIENTO" as evento , m.cliente_id, rv.precio from items_movido as im 
            left join movimiento as m on m.id == im.movimiento_id
            left join (select pv.item_id, pv.precio, m.id from precio_venta as pv 
            left join items_movido im on im.item_id = pv.item_id
            left join movimiento as m on m.id == im.movimiento_id and m.fecha between pv.fecha_inicio and ifnull(pv.fecha_final,'2999-12-31'))
             as rv on rv.item_id == im.item_id and rv.id == m.id where im.item_id==%d
            union
            select item_id, cantidad, "NONE", fecha, "VENTA", cliente_id, precio from venta as v where v.item_id==%d
            order by fecha
            
            """ % (self.id, self.id)

            results = conn.execute(text(sql))
            obj_result = []
            session = db.session()
            for r in results:
                o = type('', (), {})()
                o.cliente = session.query(Cliente).filter(Cliente.id == r['cliente_id']).one()
                o.cantidad = r['cantidad']
                o.tipo = r['evento']
                o.valor = r['precio']
                o.fecha = datetime.strptime(r['fecha'], '%Y-%m-%d %H:%M:%S.%f')
                obj_result.append(o)

            return obj_result

    @staticmethod
    def getItemsByClient(procedencia):
        # TODO: Make this from another way. This is for going fast and is a shit

        engine = db.Engine.instance
        with engine.connect() as conn:
            sql = """ select r1.item_id, (ifnull(r1.total_sal,0) - ifnull(r2.total_dev,0) - ifnull(rv.vendido,0)) as tiene, r1.cliente_id
            from (select im.item_id, m.tipo, c.nombre, sum(im.cantidad) as total_sal, m.cliente_id from movimiento as m 
            left join items_movido as im on im.movimiento_id == m.id 
            left join item as i on i.id == im.item_id
            left join cliente as c on c.id == m.cliente_id
            where m.tipo = "SALIDA" and i.procedencia_id == %d group by im.item_id, m.tipo,m.cliente_id) as r1
            
            left join (select im.item_id, m.tipo, c.nombre, sum(im.cantidad)as total_dev, m.cliente_id  from movimiento as m
            left join items_movido as im on im.movimiento_id == m.id left join cliente as c on c.id == m.cliente_id 
            where m.tipo = "DEVOLUCION" group by im.item_id, m.tipo) as r2 on r1.item_id == r2.item_id and r1.cliente_id == r2.cliente_id 
            left join item on item.id == r1.item_id          
            left join (select v.item_id, v.cliente_id, sum(v.cantidad) as vendido from venta as v group by v.item_id, v.cliente_id) as rv 
            on r1.item_id == rv.item_id and r1.cliente_id == rv.cliente_id
            where tiene > 0;
                    """ % procedencia

            results = conn.execute(text(sql))
            res = []
            items_id = []
            clients_id = []
            for row in results:
                items_id.append(row['item_id'])
                clients_id.append(row['cliente_id'])
                res.append((row['item_id'], row['cliente_id'], row['tiene']))

            session = db.session()
            items = session.query(Item).filter(Item.id.in_(items_id)).all()

            clientes = session.query(Cliente).filter(Cliente.id.in_(clients_id)).all()

            obj_res = []
            for r in res:
                o = type('', (), {})()
                for i in items:
                    if i.id == r[0]:
                        o.item = i
                for c in clientes:
                    if c.id == r[1]:
                        o.cliente = c
                o.tiene = r[2]
                obj_res.append(o)
            return obj_res

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

    def getPrecioinDate(self, fecha=datetime.date(datetime.now())):
        for p in self.precio:
            if p.fecha_inicio is None or p.fecha_final is None:
                continue
            if p.fecha_inicio < fecha < p.fecha_final:
                return p
        return self.precio[-1]

    def __repr__(self):
        return "Item<-%s-,'%s'>" % (self.id, self.cantidad)
    
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
            sql = """ select r1.item_id, (ifnull(r1.total_sal,0) - ifnull(r2.total_dev,0) - ifnull(rv.vendido,0)) as tiene
            from (select im.item_id, m.tipo, c.nombre, sum(im.cantidad) as total_sal, m.cliente_id from movimiento as m 
            left join items_movido as im on im.movimiento_id == m.id left join cliente as c on c.id == m.cliente_id
            where m.tipo = "SALIDA" and c.id == %d group by im.item_id, m.tipo,m.cliente_id) as r1
            left join (select im.item_id, m.tipo, c.nombre, sum(im.cantidad)as total_dev, m.cliente_id  from movimiento as m
            left join items_movido as im on im.movimiento_id == m.id left join cliente as c on c.id == m.cliente_id 
            where m.tipo = "DEVOLUCION" group by im.item_id, m.tipo) as r2 on r1.item_id == r2.item_id and r1.cliente_id == r2.cliente_id 
            left join item on item.id == r1.item_id          
            left join (select v.item_id, v.cliente_id, sum(v.cantidad) as vendido from venta as v 
            where v.cliente_id == %d
            group by v.item_id) as rv on r1.item_id == rv.item_id
            where tiene > 0;
                    """ % (self.id, self.id)

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

    def __repr__(self):
        return "Cliente<-%s-,'%s','%s'>" % (self.id, self.nombre, self.tipo)


# ----------------------------------------------GASTOS------------------------------------------------
class Gasto(Base):
    """Gatos de viaje"""

    def __init__(self, ):
        Base.__init__(self)

    __tablename__ = "gasto"

    id = Column(Integer, primary_key=True)
    procedencia_id = Column(Integer, ForeignKey('procedencia.id'))
    procedencia = relationship("Procedencia", backref="gastos")

    cantidad = Column(Float)
    descripcion = Column(String(250))

    def __repr__(self):
        return "Gasto<-%s-,'%.2f'>" % (self.id, self.cantidad)
