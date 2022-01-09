import sqlite3

con = sqlite3.connect('villager-trade-tracker.sqlite3')
cur = con.cursor()

cur.execute('''CREATE TABLE villagers
				(id, name, type, level, user);''')

con.commit()

cur.execute('''CREATE TABLE users
				(id, username)''')

con.commit()

con.close()