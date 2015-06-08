#!/usr/bin/env python
#
# Python2/3 compatible
# Openssl compatible, decrypt using
# $ openssl aes-256-cbc -d -in ./file.enc -out ./file.dec

from hashlib import md5
from Crypto.Cipher import AES
from os import urandom

def derive_key_and_iv(password, salt, key_length, iv_length):

    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + str.encode(password) + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, salt_header='Salted__', key_length=32):
    """ AES encrypt an open file object.

    salt_header default "Salted__" compatible with openssl implementation."""

    bs = AES.block_size
    salt = urandom(bs - len(salt_header))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write(str.encode(salt_header) + salt)
    fin = False
    while not fin:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            fin= True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, salt_header='Salted__', key_length=32):
    """ AES decrypt an open file object.

    salt_header default "Salted__" compatible with openssl implementation."""

    bs = AES.block_size
    salt = in_file.read(bs)[len(salt_header):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    fin = False
    while not fin:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = chunk[-1]
            print(type(padding_length))
            if not type(padding_length) == int:
                padding_length = ord(padding_length)
            #print(" ".join("{:02x}".format(ord(c)) for c in padding_length))
            chunk = chunk[:-padding_length]
            fin= True
        out_file.write(bytes(b for b in chunk))

if __name__ == '__main__':

    with open('./wallet', 'rb') as fin, open('./wallet.enc', 'wb') as fout:
        encrypt(fin, fout, 'this is a test')

    import base64
    with open('./wallet.enc', 'rb') as fin, open('./wallet.enc.b64', 'wb') as fout:
        base64.encode(fin, fout)

    with open('./wallet.enc.b64', 'rb') as fin, open('./wallet.enc2', 'wb') as fout:
        base64.decode(fin, fout)

    with open('./wallet.enc2', 'rb') as fin, open('./wallet.dec', 'wb') as fout:
        decrypt(fin, fout, 'this is a test')

