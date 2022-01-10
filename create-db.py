import sqlite3
import uuid
import secrets
import pyotp

con = sqlite3.connect('villager-trade-tracker.sqlite3')
cur = con.cursor()

cur.execute('''CREATE TABLE villagers
(id type UNIQUE, name, type, level, user, zombied);''')

cur.execute('''CREATE TABLE users
(id type UNIQUE, password, otp, sql_privilege);''')

cur.execute('''CREATE TABLE tokens
(user_id, token type UNIQUE, expire);''')

cur.execute('''CREATE TABLE trades
(id type UNIQUE, villager_id, item_wanted, quantity_wanted, item_given, quantity_given, lockout, xp_given);''')

if input('''Include Testing Data?
WARNING: POTENTIALLY DANGEROUS
Type "CONFIRMDEVENV" to include.''') == "CONFIRMDEVENV":
	print('Creating test values')
	test_account_id = '05996afc6b0f4a54a81f55957155b60d'
	test_account_pw = 'password'
	test_account_otp = 'U4NOUGHP3FH36IXZ7OC63YC63GVHXXB7'
	cur.execute(f'''INSERT INTO users
	(id, password, otp, sql_privilege) VALUES
	('{test_account_id}', '{test_account_pw}', '{test_account_otp}', TRUE);''')
	totp = pyotp.TOTP(test_account_otp)
	print("Username:",test_account_id)
	print("Password:",test_account_pw)
	print("OTP:",totp.provisioning_uri(issuer_name='villager-trade-tracker'))
	
	test_villagers = [
		["TH1","Shepherd",5],
		["TH2","Cleric",5]
	]

	for v in test_villagers:
		cur.execute(f'''INSERT INTO villagers
		(id, name, type, level, user, zombied) VALUES
		('{uuid.uuid4().hex}', '{v[0]}', '{v[1]}', '{v[2]}', '{test_account_id}', 0);''')

con.commit()

con.close()