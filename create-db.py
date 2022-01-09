import sqlite3
import uuid
import secrets
import pyotp

con = sqlite3.connect('villager-trade-tracker.sqlite3')
cur = con.cursor()

cur.execute('''CREATE TABLE villagers
(id, name, type, level, user);''')

cur.execute('''CREATE TABLE users
(id, otp, sql_privilege);''')

cur.execute('''CREATE TABLE tokens
(id, username, token);''')

if input('''Include Testing Data?
WARNING: POTENTIALLY DANGEROUS
Type "CONFIRMDEVENV" to include.''') == "CONFIRMDEVENV":
	print('Creating test values')
	test_account_id = '05996afc6b0f4a54a81f55957155b60d'
	test_account_otp = 'U4NOUGHP3FH36IXZ7OC63YC63GVHXXB7'
	cur.execute(f'''INSERT INTO users
	(id, otp, sql_privilege) VALUES
	('{test_account_id}', '{test_account_otp}', TRUE);''')
	totp = pyotp.TOTP(test_account_otp)
	print(test_account_id,totp.provisioning_uri(issuer_name='villager-trade-tracker'))

con.commit()

con.close()