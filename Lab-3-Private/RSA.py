import random

ef gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    a1, a2, a3 = 1, 0, phi
    b1, b2, b3 = 0, 1, e
    while b3 != 0:
        q = a3 // b3
        t1 = a1 - q * b1
        t2 = a2 - q * b2
        t3 = a3 - q * b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3
    if a2 < 0:
        a2 = a2 + phi
    return a2


def is_prime(num):
    """
    Check if a number is prime.
    """
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while gcd(e, phi) != 1:
        e += 2
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    """
    key, n = pk
    cipher = []
    for ch in plaintext:
        cipher.append(pow(ord(ch), key, n))
    return cipher


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    """
    key, n = pk
    plain = ""
    for c in ciphertext:
        plain += chr(pow(c, key, n))
    return plain

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
