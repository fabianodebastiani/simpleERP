# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('assistente.db')
c = conn.cursor()


sqlString = 'SELECT SUM(valorDaNota) FROM notas WHERE natureza=?'

c.execute(sqlString, ("RETORNO DE CONSERTO",))
print(c.fetchall())

conn.close()