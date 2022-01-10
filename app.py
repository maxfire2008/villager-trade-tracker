import sqlite3
import flask
import secrets
import pyotp
import time
import json

from create_otp_qr import create_otp_qr

TEXTURES = json.loads(open("textures.json","rb").read())
TEXT_LOOKUP = json.loads(open("text.json","rb").read())

def get_villager_texture_url(name):
	name=name.lower()
	if name in TEXTURES["profession"]:
		return "/static/"+TEXTURES["profession"][name.lower()]
	return "/static/textures/block/bedrock.png"

def get_villager_level(level):
	level=str(level)
	if level in TEXT_LOOKUP["xp_levels"]:
		return TEXT_LOOKUP["xp_levels"][level]
	return level

def get_item_texture_url(name):
	name=name.lower()
	if name in TEXTURES["item"]:
		return "/static/"+TEXTURES["item"][name.lower()]
	return "/static/textures/block/bedrock.png"

def get_user(token):
	con = sqlite3.connect('villager-trade-tracker.sqlite3')
	cur = con.cursor()

	user_id = ""
	expire = 0
	for row in cur.execute('SELECT user_id, expire FROM tokens WHERE token == (?);',[token]):
		user_id = row[0]
		expire = row[1]

	if expire < int(time.time()):
		cur.execute('DELETE FROM tokens WHERE token == (?);',[token])
		return None

	con.commit()
	con.close()
	return user_id

app = flask.Flask(__name__)

@app.route("/")
def index():
	token = flask.request.cookies.get('token','')
	user_id=get_user(token)
	return flask.render_template('index.html',user_id=user_id)

@app.route("/list/")
def list():
	token = flask.request.cookies.get('token','')
	user_id=get_user(token)
	if user_id:
		con = sqlite3.connect('villager-trade-tracker.sqlite3')
		cur = con.cursor()

		villagers = []

		for row in cur.execute('SELECT id, name, type, level FROM villagers WHERE user == (?);',[user_id]):
			villagers.append({
				"id": row[0],
				"name": row[1],
				"type": row[2],
				"level": row[3],
				"texture": get_villager_texture_url(row[2]),
				"level_text": get_villager_level(row[3])
			})

		con.commit()
		con.close()
		return flask.render_template('list.html',user_id=user_id,villagers=villagers)
	return flask.redirect("/login/?redirect="+"/list/", code=302)

@app.route("/view_villager/<villager>")
def view_villager(villager):
	token = flask.request.cookies.get('token','')
	user_id=get_user(token)
	if user_id:
		con = sqlite3.connect('villager-trade-tracker.sqlite3')
		cur = con.cursor()

		trades = []

		for row in cur.execute(
		'''SELECT id, item_wanted, quantity_wanted, item_given, quantity_given, lockout, xp_given
FROM trades WHERE villager_id == (?);''',[villager]):
			trades.append({
				"id": row[0],
				"wanted_item": row[1],
				"wanted_count": row[2],
				"given_item": row[3],
				"given_count": row[4],
				"lockout": row[5],
				"xp_given": row[6],
				"wanted_item_texture": get_item_texture_url(row[1]),
				"given_item_texture": get_item_texture_url(row[3])
			})

		con.commit()
		con.close()
		return flask.render_template('view_villager.html',user_id=user_id,trades=trades,villager_id=villager)
	return flask.redirect("/login/?redirect="+"/view_villager/"+villager, code=302)

@app.route("/qr_code/<key>/")
def qr_code(key):
	otp_qr = create_otp_qr(key)
	print(type(otp_qr))
	return flask.send_file(otp_qr, mimetype='image/png')

@app.route("/login/")
def login():
	return flask.render_template('login.html',
	redirect=flask.request.args.get("redirect","/"),
	failure=flask.request.args.get("failure",False))

@app.route("/login_submit/", methods = ['POST'])
def login_submit():
	username = flask.request.form.get('username')
	password = flask.request.form.get('password')
	otp = flask.request.form.get('otp')
	redirect = flask.request.form.get('redirect')

	con = sqlite3.connect('villager-trade-tracker.sqlite3')
	cur = con.cursor()

	key = ""
	pw = ""
	for row in cur.execute('SELECT otp, password FROM users WHERE id == (?);',[username]):
		key = row[0]
		pw = row[1]
	print(key)
	totp = pyotp.TOTP(key)
	TOKEN_AGE = 7*24*60*60
	if totp.verify(otp) and password == pw:
		token_expiry = int(time.time())+TOKEN_AGE

		token_generated = secrets.token_hex(32)

		resp = flask.redirect(redirect, code=302)
		resp.set_cookie('token', token_generated, max_age=TOKEN_AGE)
		cur.execute(f'''INSERT INTO tokens
		(user_id, token, expire) VALUES
		('{username}', '{token_generated}', {token_expiry});''')
		con.commit()
		con.close()
		return resp
	else:
		return flask.redirect("/login/?redirect="+redirect+"&failure=True", code=302)

@app.route("/logout/", methods = ['GET','POST'])
def logout():
	token = flask.request.cookies.get('token')
	user_id=None
	if token:
		user_id=get_user(token)
	if user_id:
		con = sqlite3.connect('villager-trade-tracker.sqlite3')
		cur = con.cursor()

		cur.execute('DELETE FROM tokens WHERE user_id == (?);',[user_id])

		con.commit()
		con.close()
	return flask.redirect("/", code=302)