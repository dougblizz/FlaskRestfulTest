# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect("MyDB.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)



connection.commit()

connection.close()

