# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('assistente.db')
c = conn.cursor()


sqlString = "SELECT * FROM notas WHERE valorDaNota > 100000"

c.execute(sqlString)
print(c.fetchall())

conn.close()