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
(id type UNIQUE, villager_id, item_wanted, quantity_wanted, item_given, quantity_given, lockout, xp_given, zombied_multi);''')

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
		["TH2","Cleric",5],
		["TH3","Fisherman",4],
		["TH4","Librarian",3],
		["TH5","Mason",2],
		["TH6","Fletcher",1]
	]

	for v in test_villagers:
		cvill_id = uuid.uuid4().hex
		cur.execute(f'''INSERT INTO villagers
		(id, name, type, level, user, zombied) VALUES
		('{cvill_id}', '{v[0]}', '{v[1]}', '{v[2]}', '{test_account_id}', 0);''')
		cur.execute(f'''INSERT INTO trades
		(id, villager_id, item_wanted, quantity_wanted, item_given, quantity_given, lockout, xp_given, zombied_multi) VALUES
		('{uuid.uuid4().hex}', '{cvill_id}', 'Coal', 15, 'Emerald', 1, 16, 2, 5);''')

	print('Creating Eve')
	test_account_id = 'aaf08af36f8643db81fc040d09f78ebe'
	test_account_pw = '12345678'
	test_account_otp = 'ZUPGKLOFUE3G7NZV4VTHBRVYYCY4Y36N'
	cur.execute(f'''INSERT INTO users
	(id, password, otp, sql_privilege) VALUES
	('{test_account_id}', '{test_account_pw}', '{test_account_otp}', TRUE);''')
	totp = pyotp.TOTP(test_account_otp)
	print("Eve Username:",test_account_id)
	print("Eve Password:",test_account_pw)
	print("Eve OTP:",totp.provisioning_uri(issuer_name='villager-trade-tracker'))

con.commit()

con.close()