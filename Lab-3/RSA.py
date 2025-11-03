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
    # TODO: implement Euclidean algorithm
   
    if (a == 0):
      return b

    return gcd(b%a, a)
    pass

def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # TODO: implement Extended Euclidean Algorithm
    x = 0
    y = 1
    ph = phi
    prev_x = 1
    prev_y = 0
    

    while phi != 0:
      remainder = e // phi
      e = phi
      phi = e % phi
      prev_x = x
      x = prev_x - remainder * x
      prev_y = y
      y = prev_y - remainder * y

    if prev_x < 0:
      prev_x += ph

    return prev_x


    pass


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # TODO: implement primality check

    if (num % 2 == 0):
      return False

    i = 3
    while i*i <= num:
      if num %i ==0:
        return False
      i += 2
    return True

    pass


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    # TODO: implement RSA keypair generation
    # Steps:
    # 1. Compute n = p * q
    # 2. Compute phi = (p-1)*(q-1)
    # 3. Choose e such that gcd(e, phi) = 1
    # 4. Compute d = multiplicative_inverse(e, phi)

    n = p*q
    phi = (p-1)*(q-1)
    e = random.randrange(2, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

    pass


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    key, n = pk
    ciphertext = [(ord(char) ** key) % n for char in plaintext]
    return ciphertext"""
    # TODO: implement RSA encryption

    e,n = pk
    c = [(ord(char) ** e) % n for char in plaintext]
    return p
    pass


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # TODO: implement RSA decryption
    d, n = pk
    p = [chr((char ** d) % n) for char in ciphertext]
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


