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
    
    while b != 0:
        a,b=b, a % b
    return abs(a)


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # TODO: implement Extended Euclidean Algorithm
    old_x, x = e, phi
    old_y, y = 1, 0
    old_z, z = 0, 1

    while x != 0:
        remainder = old_x // x
        old_x,x = x, old_x - remainder * x
        old_y,y = y, old_y - remainder * y
        old_z,z = z, old_z - remainder * z

    if old_x != 1:
        temp = old_y % phi
    return temp


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # TODO: implement primality check
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
    # TODO: implement RSA keypair generation
    # Steps:
    # 1. Compute n = p * q
    # 2. Compute phi = (p-1)*(q-1)
    # 3. Choose e such that gcd(e, phi) = 1
    # 4. Compute d = multiplicative_inverse(e, phi)
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
    # TODO: implement RSA encryption
    k,n = pk
    return [pow(ord(ch),k,n) for ch in plaintext]
    pass


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # TODO: implement RSA decryption
    k,n = pk
    chars = [chr(pow(c,k,n)) for c in ciphertext]
    return "".join(chars)
    


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
