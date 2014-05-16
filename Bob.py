#!/usr/bin/env python
# Encryption Server
import socket
from Crypto.Hash import SHA
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA
import pickle
import base64

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
pubkey = open("cs4480/pa3/bob/publickey.pem","r").read()
prikey = open("cs4480/pa3/bob/privatekey.pem","r").read()
rsapubkey = RSA.importKey(pubkey)
rsaprikey = RSA.importKey(prikey)
#rsakey = RSA.generate(1024)
#print('Connected by ' + "".join(addr))
while 1:
    data = conn.recv(1024)
    if not data: break
    print('Server received '+ str(data))
    if(data == b'Hello Client'):
    	conn.sendall(b'Hello Server')
    print('Server sending key: ' + str(pickle.dumps(rsapubkey)))
    conn.sendall(pickle.dumps(rsapubkey))
    iv = conn.recv(8)
    print('Server received iv: ' + str(iv))
    symkeyexch = conn.recv(1024)
    symkey = rsaprikey.decrypt(symkeyexch)
    lens = len(symkey)
    lenx = lens-lens%4
    passkey = base64.b64decode(symkey[:lenx])
    print('Server received symkey ' + str(passkey))
conn.close()
