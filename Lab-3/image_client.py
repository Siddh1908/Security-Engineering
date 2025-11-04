"""
image_client.py
Lab: Secure Image Transfer with RSA, DES, and Raspberry Pi GPIO
---------------------------------------------------------------

Your tasks:
- Use your RSA implementation to encrypt the DES key
- Use your DES implementation to encrypt the image
- Send the encrypted key and image to the server
- Buzz when the image is sent
"""

import socket
import time
import lgpio

from RSA import generate_keypair  # NOTE: encrypt used with PRIVATE for server to verify via PUBLIC
from des import des

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for the buzzer
BUZZER_PIN = 27  # [FIX in TODO]
# TODO: Open gpiochip and claim output for the buzzer
h = lgpio.gpiochip_open(0)  # [FIX in TODO]
lgpio.gpio_claim_output(h, BUZZER_PIN, 0)  # [FIX in TODO]

def buzz(duration=0.3):
    """TODO: Buzzer ON -> sleep -> OFF"""
    # [FIX in TODO]
    lgpio.gpio_write(h, BUZZER_PIN, 1)
    time.sleep(duration)
    lgpio.gpio_write(h, BUZZER_PIN, 0)

# --- RSA setup ---
p, q = 3557, 2579
public, private = generate_keypair(p, q)  # public=(e,n), private=(d,n)

# --- DES setup ---
cipher = des()
des_key = "8bytekey"  # must be 8 chars

# Load image as bytes, then map bytes→text losslessly via latin-1
with open("penguin.jpg", "rb") as f:
    image_bytes = f.read()

# TODO: Convert image_bytes to string (latin-1 safe)
image_text = image_bytes.decode("latin-1")  # [FIX in TODO]
# TODO: Encrypt with DES (use padding=True, cbc=True)
des_encrypted = cipher.encrypt(des_key, image_text, padding=True, cbc=True)  # [FIX in TODO]
# TODO: Encrypt DES key with RSA
# We encrypt with our PRIVATE so the server can recover it with our PUBLIC it received.
rk, n = private
rsa_encrypted_key = [pow(ord(ch), rk, n) for ch in des_key]

# --- Socket setup ---
HOST = "127.0.0.1"
PORT = 6000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[image_client] Connected to {HOST}:{PORT}")

    # Step 1: Send RSA public key
    # TODO
    e, n = public  # [FIX in TODO]
    client.sendall(f"KEY:{e},{n}\n".encode("utf-8"))  # [FIX in TODO]
    print("[image_client] Sent public key.")

    # Step 2: Send encrypted DES key
    # TODO
    key_payload = ",".join(map(str, rsa_encrypted_key))  # [FIX in TODO]
    client.sendall(f"DESKEY:{key_payload}\n".encode("utf-8"))  # [FIX in TODO]
    print("[image_client] Sent RSA-encrypted DES key.")

    # Step 3: Send encrypted image
    # TODO
    img_payload = ",".join(str(ord(c)) for c in des_encrypted)  # [FIX in TODO]
    client.sendall(f"IMAGE:{img_payload}\n".encode("utf-8"))  # [FIX in TODO]
    print("[image_client] Sent DES-encrypted image.")

    # Feedback
    buzz()

    client.close()
    lgpio.gpio_free(h, BUZZER_PIN)
    lgpio.gpiochip_close(h)
    print("[image_client] Closed connection and cleaned up GPIO.")

if __name__ == "__main__":
    main()
