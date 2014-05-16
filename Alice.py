#!/usr/bin/env python
# Encryption Client
import socket
from Crypto.Hash import SHA
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util import randpool
import pickle
import base64

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
sh = SHA.new()
file = open('md.txt', 'r')
text = file.read()
blah = randpool.RandomPool()
RSAKey = RSA.generate(1024, blah.get_bytes)
#sh.update(text)
iv = Random.get_random_bytes(8)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Hello Client')
data = s.recv(1024)
print('Received from server ' + str(data))
if(data == b'Hello Server'):
	key = s.recv(1024)
	print('Client received key: ' + str(key))
bobkey = pickle.loads(key)
print('Client sends iv : ' + str(iv))
s.sendall(iv);
symkey = "passwordpassword"
passkey = base64.b64encode(symkey.encode('utf_8'))
des = DES3.new(symkey, DES3.MODE_CBC, iv)
symkeyexch = RSAKey.encrypt(passkey, 32)
print('Client sends symkey : ' + str(symkeyexch[0]))
s.sendall(symkeyexch[0])
s.close()