# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('assistente.db')
c = conn.cursor()

string = "NFe35210102702284000274550200001223641687286672"

c.execute("""SELECT EXISTS(SELECT 1 FROM notas WHERE id=?)""",(string,))
print(c.fetchall())

conn.close()