import sqlite3
import flask

from create_otp_qr import create_otp_qr

con = sqlite3.connect('villager-trade-tracker.sqlite3')
cur = con.cursor()

app = flask.Flask(__name__)

@app.route("/")
def index():
	token = flask.request.cookies.get('token')
	signed_in=False
	if token:
		signed_in=True
	return flask.render_template('index.html',signed_in=signed_in)

@app.route("/qr_code/<key>")
def qr_code(key):
	otp_qr = create_otp_qr(key)
	print(type(otp_qr))
	return flask.send_file(otp_qr, mimetype='image/png')

@app.route("/login")
def login():
	return flask.render_template('login.html',signed_in=token)

@app.route("/login_submit", methods = ['POST'])
def login_submit():
	return ""
