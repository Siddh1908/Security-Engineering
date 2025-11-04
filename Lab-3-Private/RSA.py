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
import math

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    # TODO: implement Euclidean algorithm
    # [FIX in TODO]
    while b != 0:
        a, b = b, a % b
    return abs(a)


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # TODO: implement Extended Euclidean Algorithm
    # [FIX in TODO]
    old_r, r = e, phi
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    # old_r = gcd(e, phi) should be 1
    if old_r != 1:
        raise ValueError("e and phi are not coprime; inverse does not exist")
    d = old_s % phi
    return d


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # TODO: implement primality check
    # [FIX in TODO]
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0:
        return False
    limit = int(math.isqrt(num))
    for i in range(3, limit + 1, 2):
        if num % i == 0:
            return False
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
    # [FIX in TODO]
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p and q must be prime")
    if p == q:
        raise ValueError("p and q cannot be equal")
    n = p * q
    phi = (p - 1) * (q - 1)
    # pick e
    e = 65537
    if gcd(e, phi) != 1:
        # fallback to random odd e
        e = random.randrange(3, phi - 1, 2)
        while gcd(e, phi) != 1:
            e = random.randrange(3, phi - 1, 2)
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    # TODO: implement RSA encryption
    # [FIX in TODO]
    k, n = pk
    return [pow(ord(ch), k, n) for ch in plaintext]


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # TODO: implement RSA decryption
    # [FIX in TODO]
    k, n = pk
    chars = [chr(pow(c, k, n)) for c in ciphertext]
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
