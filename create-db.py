import sqlite3

con = sqlite3.connect('villager-trade-tracker.db')
cur = con.cursor()

cur.execute('''CREATE TABLE villagers
				(id, name, type, level, user)''')

cur.execute('''CREATE TABLE users
				(id, username, 2facode''')