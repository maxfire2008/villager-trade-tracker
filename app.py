import sqlite3
import flask
import secrets
import pyotp

from create_otp_qr import create_otp_qr

app = flask.Flask(__name__)

@app.route("/")
def index():
	token = flask.request.cookies.get('token')
	signed_in=False
	if token:
		signed_in=True
	return flask.render_template('index.html',signed_in=signed_in)

@app.route("/qr_code/<key>/")
def qr_code(key):
	otp_qr = create_otp_qr(key)
	print(type(otp_qr))
	return flask.send_file(otp_qr, mimetype='image/png')

@app.route("/login/")
def login():
	return flask.render_template('login.html')

@app.route("/login_submit/", methods = ['POST'])
def login_submit():
	username = flask.request.form.get('username')
	otp = flask.request.form.get('otp')

	con = sqlite3.connect('villager-trade-tracker.sqlite3')
	cur = con.cursor()

	key = ""
	for row in cur.execute(f'SELECT otp FROM users WHERE id == "{username}"'):
		key = row[0]

	totp = pyotp.TOTP(key)
	if totp.verify(otp):
		token_generated = secrets.token_hex(32)

		resp = flask.redirect("/", code=302)
		resp.set_cookie('token', token_generated)
		cur.execute(f'''INSERT INTO tokens
		(user_id, token) VALUES
		('{username}', '{token_generated}');''')
		con.commit()
		con.close()
		return resp
	else:
		return flask.redirect("/login/", code=401)
