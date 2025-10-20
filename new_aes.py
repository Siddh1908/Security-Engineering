import os
from Crypto.Cipher import AES

BLOCK = 16

def pad(b):
    """Pad data so length is a multiple of 16 bytes."""
    pad_len = BLOCK - (len(b) % BLOCK)
    return b + bytes([pad_len] * pad_len)

def unpad(b):
    """Remove padding added by pad()."""
    pad_len = b[-1]
    return b[:-pad_len]

def encrypt_ecb_blocks(pt, key):
    """Encrypt data with AES in ECB mode."""
    cipher = AES.new(key, AES.MODE_ECB)
    pt_padded = pad(pt)
    return cipher.encrypt(pt_padded)

def decrypt_ecb_blocks(ct, key):
    """Decrypt data with AES in ECB mode."""
    cipher = AES.new(key, AES.MODE_ECB)
    pt_padded = cipher.decrypt(ct)
    return unpad(pt_padded)

def encrypt_cbc_blocks(pt, key):
    """Encrypt data with AES in CBC mode, return (iv, ciphertext)."""
    iv = os.urandom(BLOCK)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_padded = pad(pt)
    ct = cipher.encrypt(pt_padded)
    return iv, ct

def decrypt_cbc_blocks(iv, ct, key):
    """Decrypt data with AES in CBC mode."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    return unpad(pt_padded)
