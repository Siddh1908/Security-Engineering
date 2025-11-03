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
    # Euclidean algorithm (iterative)
    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # Extended Euclidean Algorithm
    orig_phi = phi
    a, b = e, phi
    x0, x1 = 1, 0  # coefficients for a
    y0, y1 = 0, 1  # coefficients for b

    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    # a is gcd(e, phi). Inverse exists only if gcd == 1
    if a != 1:
        raise ValueError("e and phi are not coprime; inverse does not exist")
    return x0 % orig_phi


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime.")
    if p == q:
        raise ValueError("p and q cannot be the same.")

    # 1. n = p * q
    n = p * q
    # 2. phi = (p-1)*(q-1)
    phi = (p - 1) * (q - 1)
    # 3. Choose e such that gcd(e, phi) = 1
    e = 65537
    if e >= phi or gcd(e, phi) != 1:
        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)
    # 4. d = multiplicative_inverse(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    key, n = pk
    return [pow(ord(char), key, n) for char in plaintext]


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    key, n = pk
    # Allow a single int ciphertext, or a list
    if isinstance(ciphertext, int):
        ciphertext = [ciphertext]
    plain_chars = [chr(pow(c, key, n)) for c in ciphertext]
    return ''.join(plain_chars)


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
