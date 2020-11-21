import os
# security imports
import base64 
from cryptography.fernet import Fernet
from passlib.hash import argon2

# generate key and pepper
# add: store in secure location
key = Fernet.generate_key()
pep = Fernet(key)

# hash the given password using the pepper
# returns the hashed password
def hash_password(pwd, pep):
    h = argon2.using(rounds=10).hash(pwd)
    ph = pep.encrypt(h.encode('utf-8'))
    b64ph = base64.b64encode(ph)
    return b64ph

# check if given password matches the encrypted b64ph password
# returns true if match, else returns false
def check_password(pwd, b64ph, pep):
    ph = base64.b64decode(b64ph)
    h = pep.decrypt(ph)
    return argon2.verify(pwd, h)

dbpwd = "thisisapassword"
hpwd = hash_password(dbpwd, pep)
d_hpwd = hpwd.decode('utf-8')
print(type(hpwd))
print(hpwd)
print(type(d_hpwd))
print(d_hpwd)
encode_pwd = d_hpwd.encode('utf-8')
print(type(encode_pwd))
print(encode_pwd)
if hpwd == encode_pwd:
    print("decode-encode success")

