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

from RSA import generate_keypair
from des import des

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for the buzzer
# TODO: Open gpiochip and claim output for the buzzer
BUZZER_PIN = 27
h = lgpio.gpiochip_open(0)


# TODO: Open gpiochip and claim output for the buzzer
lgpio.gpio_claim_output(h, BUZZER_PIN)

def buzz(duration=0.3):
    """TODO: Buzzer ON -> sleep -> OFF"""
    lgpio.gpio_write(h, BUZZER_PIN, 1)
    time.sleep(duration)
    lgpio.gpio_write(h, BUZZER_PIN, 0)
    pass

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
image_text = image_bytes.decode("latin-1")
# TODO: Encrypt with DES (use padding=True, cbc=True)
des_encrypted = cipher.encrypt(image_text, des_key, padding=True, cbc=True)
# TODO: Encrypt DES key with RSA
from RSA import encrypt as rsa_encrypt
rsa_encrypted_des_key = rsa_encrypt(public, des_key)

# --- Socket setup ---
HOST = "127.0.0.1"
PORT = 6000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[image_client] Connected to {HOST}:{PORT}")

    # Step 1: Send RSA public key
    # TODO
    e, n = public
    client.sendall(f"KEY:{e},{n}\n".encode("utf-8"))

    # Step 2: Send encrypted DES key
    # TODO
    deskey_payload = "DESKEY:" + ",".join(str(x) for x in rsa_encrypted_des_key) + "\n"
    client.sendall(deskey_payload.encode("utf-8"))

    # Step 3: Send encrypted image
    # TODO
    des_bytes = des_encrypted.encode("latin-1")
    client.sendall(f"IMG_LEN:{len(des_bytes)}\n".encode("utf-8"))
    client.sendall(des_bytes)

    # Feedback
    buzz()

    client.close()
    lgpio.gpio_free(h, BUZZER_PIN)
    lgpio.gpiochip_close(h)
    print("[image_client] Closed connection and cleaned up GPIO.")

if __name__ == "__main__":
    main()
