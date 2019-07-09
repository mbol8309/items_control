import unittest
from items_control.data import db
from items_control import orm
import os
import sqlite3

class TestDB(unittest.TestCase):

    def test_db_create(self):
        filename = os.tmpfile()
        db.create_db(filename)
        cliente = orm.Cliente()
        cliente.nombre = "cliente"
        cliente.direccion = "somewhere"
        cliente.telefono = '555'
        cliente.tipo = orm.TipoClienteEnum.MAYORITARIO
        session = db.session()
        session.add(cliente)
        session.commit()

        #test input with sqlite
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        result = c.execute('select * from cliente')
        r = result.fetchone()
        self.assertEqual(r[1],cliente.nombre)
        self.assertEqual(r[2],cliente.telefono)
        self.assertEqual(r[3],cliente.direccion)
        self.assertEqual(r[4],cliente.tipo.name)

if __name__ == '__main__':
    unittest.main()