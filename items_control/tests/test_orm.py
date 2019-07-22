from items_control import orm
from items_control.data import db
import unittest
import datetime

db.open_db("/home/mbolivar/Projects/items_control/items_control/data/db.sqlite", True)

session = db.session()

# m = orm.Movimiento()
# m.tipo = orm.TipoMovimiento.SALIDA
# m.fecha = datetime.datetime.now()
#
# i = session.query(orm.Item).first()
#
# itemsmovido = orm.ItemMovido()
# itemsmovido.cantidad=2
# itemsmovido.item = i
# m.items.append(itemsmovido)
#
# session.add(m)
# session.commit()

items = session.query(orm.Item).all()

print items
