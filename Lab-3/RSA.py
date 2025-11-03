"""
RSA.py

Lab: Secure Communication with RSA, DES, and Raspberry Pi GPIO

Your task:
-----------
Implement the RSA functions below:
- gcd
- multiplicative_inverse
- is_prime
- generate_keypair
- encrypt
- decrypt

You will use these functions in both chat and image client/server code.

Notes:
- Work step by step. First get gcd() working, then move to modular inverse, etc.
- Test your implementation with the provided example at the bottom.
"""

import random

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    ph = phi
    # Extended Euclidean Algorithm using your variable names
    x, prev_x = 0, 1
    y, prev_y = 1, 0
    a, b = e, phi
    while b != 0:
        remainder = a // b
        a, b = b, a % b
        prev_x, x = x, prev_x - remainder * x
        prev_y, y = y, prev_y - remainder * y
    if a != 1:
        return None
    if prev_x < 0:
        prev_x += ph
    return prev_x

def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0:
        return False
    i = 3
    while i * i <= num:
        if num % i == 0:
            return False
        i += 2
    return True

def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    e, n = pk
    c = [pow(ord(char), e, n) for char in plaintext]
    return c

def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    d, n = pk
    if isinstance(ciphertext, int):
        ciphertext = [ciphertext]
    p = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(p)

# --- Example test case ---
if __name__ == "__main__":
    print("RSA Test Example")

    # Example primes (small for testing)
    p, q = 61, 53
    public, private = generate_keypair(p, q)

    print("Public key:", public)
    print("Private key:", private)

    message = "HELLO"
    print("Original message:", message)

    encrypted_msg = encrypt(public, message)
    print("Encrypted message:", encrypted_msg)

    decrypted_msg = decrypt(private, encrypted_msg)
    print("Decrypted message:", decrypted_msg)


