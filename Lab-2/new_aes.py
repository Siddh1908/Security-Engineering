import os
from Crypto.Cipher import AES

BLOCK = 16

def pad(b):
    """Pad data so length is a multiple of 16 bytes."""
    i = BLOCK - (len(b) % BLOCK)
    return b + bytes([i] * i)

def unpad(b):
    """Remove padding added by pad()."""
    len = b[-1]
    return b[:-len]

def encrypt_ecb_blocks(pt, key):
    """Encrypt data with AES in ECB mode."""
    data = AES.new(key, AES.MODE_ECB)
    return data.encrypt(pad(pt))

def decrypt_ecb_blocks(ct, key):
    """Decrypt data with AES in ECB mode."""
    data = AES.new(key, AES.MODE_ECB)
    return unpad(data.decrypt(ct))

def encrypt_cbc_blocks(pt, key):
    """Encrypt data with AES in CBC mode, return (iv, ciphertext)."""
    iv = os.urandom(BLOCK)
    data = AES.new(key, AES.MODE_CBC, iv)
    return iv, data.encrypt(pad(pt))

def decrypt_cbc_blocks(iv, ct, key):
    """Decrypt data with AES in CBC mode."""
    data = AES.new(key, AES.MODE_CBC, iv)
    return unpad(data.decrypt(ct))
