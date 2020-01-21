# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect('date.db')

cursor = connection.cursor()

#Crear tablas 
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

#Ejemplo para insertar un dato
user = (1, "doug", "1234")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)


#Ejemplo para insertar varios datos
users = [
    (2, "rafa", "kosa2"),
    (3, "osa", "ao23")
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()