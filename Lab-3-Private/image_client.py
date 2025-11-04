import socket
import time
import lgpio

from RSA import generate_keypair
from des import des

# --- GPIO Setup (TODO: complete this section) ---
# FIX: choose buzzer pin and claim output
BUZZER_PIN = 18
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 0, BUZZER_PIN, 0)

def buzz(duration=0.3):
    """TODO: Buzzer ON -> sleep -> OFF"""
    # FIX:
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
# FIX:
image_text = image_bytes.decode("latin-1")

# TODO: Encrypt with DES (use padding=True, cbc=True)
# IMPORTANT: des.encrypt(key, text, ...) → key first, then text
# FIX:
des_encrypted_text = cipher.encrypt(des_key, image_text, padding=True, cbc=True, IV='ASASASAS')

# TODO: Encrypt DES key with RSA
# NOTE: Server will use our PUBLIC key to "decrypt" per scaffold, so we "encrypt" with PRIVATE
# FIX: do pow with private key directly (avoids needing RSA.encrypt import)
d, n = private
enc_des_key_list = [pow(ord(ch), d, n) for ch in des_key]
enc_des_key_str = ",".join(map(str, enc_des_key_list))

# --- Socket setup ---
HOST = "127.0.0.1"
PORT = 6000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[image_client] Connected to {HOST}:{PORT}")

    # Step 1: Send RSA public key
    # FIX:
    e, nn = public
    client.sendall(f"KEY:{e},{nn}\n".encode("utf-8"))

    # Step 2: Send encrypted DES key
    # FIX:
    client.sendall(f"DESKEY:{enc_des_key_str}\n".encode("utf-8"))

    # Step 3: Send encrypted image (as comma-separated ints)
    # FIX:
    enc_img_list = [ord(ch) for ch in des_encrypted_text]  # already ciphertext as text
    enc_img_str = ",".join(map(str, enc_img_list))
    client.sendall(f"IMAGE:{enc_img_str}\n".encode("utf-8"))

    # Feedback
    buzz()

    client.close()
    lgpio.gpio_free(h, BUZZER_PIN)
    lgpio.gpiochip_close(h)
    print("[image_client] Closed connection and cleaned up GPIO.")

if __name__ == "__main__":
    main()
