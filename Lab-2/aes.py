import os
from Crypto.Cipher import AES

BLOCK = 16

def pad(b):
    """Pad data so length is a multiple of 16 bytes."""
    # TODO: append extra bytes; each added byte has value = number of bytes added

def unpad(b):
    """Remove padding added by pad()."""
    # TODO: check last byte value and strip that many bytes


def encrypt_ecb_blocks(pt, key):
    """Encrypt plaintext using AES in ECB mode with padding"""
    # TODO: check last byte value and strip that many bytes


def decrypt_ecb_blocks(ct, key):
    """Decrypt data with AES in ECB mode."""
    # TODO: decrypt then unpad


def encrypt_cbc_blocks(pt, key):
    """Encrypt data with AES in CBC mode, return (iv, ciphertext)."""
    # TODO: generate random iv, pad, encrypt using AES.MODE_CBC


def decrypt_cbc_blocks(iv, ct, key):
    """Decrypt data with AES in CBC mode."""
    # TODO: decrypt, then unpad

