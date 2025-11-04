import random

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    # FIX: Euclidean algorithm
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1
    """
    # FIX: Extended Euclidean Algorithm
    old_r, r = e, phi
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    # old_r = gcd(e,phi). if gcd != 1 there is no inverse
    if old_r != 1:
        raise ValueError("e and phi are not coprime; inverse does not exist")
    # modular inverse is old_s mod phi
    return old_s % phi

def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # FIX: simple deterministic primality for lab-sized inputs
    if num < 2:
        return False
    if num % 2 == 0:
        return num == 2
    f = 3
    while f*f <= num:
        if num % f == 0:
            return False
        f += 2
    return True

def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    # FIX: standard RSA keygen
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime")
    if p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)

    # choose e coprime to phi (common choice 65537 if coprime)
    candidate_es = [65537, 257, 17, 5, 3]
    e = None
    for ce in candidate_es:
        if ce < phi and gcd(ce, phi) == 1:
            e = ce
            break
    if e is None:
        # fallback random odd
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
    # FIX: per-character modular exponentiation
    key, n = pk
    return [pow(ord(ch), key, n) for ch in plaintext]

def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # FIX: reverse of encrypt
    key, n = pk
    return "".join(chr(pow(c, key, n)) for c in ciphertext)

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
