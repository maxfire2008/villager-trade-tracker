import sqlite3
import flask

con = sqlite3.connect('villager-trade-tracker.db')
cur = con.cursor()
