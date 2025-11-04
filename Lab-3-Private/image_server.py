"""
image_server.py
Lab: Secure Image Transfer with RSA, DES, and Raspberry Pi GPIO
---------------------------------------------------------------

Your tasks:
- Parse incoming KEY, DESKEY, and IMAGE messages
- Decrypt the DES key using RSA
- Decrypt the image using DES
- Save the decrypted image as penguin_decrypted.jpg
- Flash LED on successful decryption
"""

import socket
import time
import lgpio

from RSA import decrypt
from des import des

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for the LED
LED_PIN = 17  # [FIX in TODO]
# TODO: Open gpiochip and claim output for the LED
h = lgpio.gpiochip_open(0)  # [FIX in TODO]
lgpio.gpio_claim_output(h, LED_PIN, 0)  # [FIX in TODO]

def flash_led(times=2, duration=0.3):
    """TODO: LED ON/OFF blinking"""
    # [FIX in TODO]
    for _ in range(times):
        lgpio.gpio_write(h, LED_PIN, 1)
        time.sleep(duration)
        lgpio.gpio_write(h, LED_PIN, 0)
        time.sleep(duration)


# --- Socket setup ---
HOST = "0.0.0.0"
PORT = 6000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[image_server] Listening on {HOST}:{PORT} ...")
    conn, addr = server.accept()
    print(f"[image_server] Connected by {addr}")

    client_public_key = None  # (e, n)
    des_key = None
    des_cipher = des()

    try:
        buffer = ""
        while True:
            data = conn.recv(65536)
            if not data:
                break

            buffer += data.decode("utf-8")
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                message = message.strip()
                if not message:
                    continue

                if message.startswith("KEY:"):
                    # TODO: Parse e,n and store client_public_key
                    # [FIX in TODO]
                    _, key_str = message.split(":", 1)
                    e_str, n_str = key_str.split(",", 1)
                    client_public_key = (int(e_str), int(n_str))
                    print(f"[image_server] Received PUBLIC key: {client_public_key}")

                elif message.startswith("DESKEY:"):
                    # TODO: Decrypt DES key using RSA
                    # [FIX in TODO]
                    if client_public_key is None:
                        print("[image_server] Error: no public key yet.")
                        continue
                    _, payload = message.split(":", 1)
                    cipher_list = [int(x) for x in payload.split(",") if x]
                    des_key = decrypt(client_public_key, cipher_list)
                    print("[image_server] Recovered DES key.")

                elif message.startswith("IMAGE:"):
                    if des_key is None:
                        print("[image_server] Error: no DES key yet.")
                        continue
                    # TODO: Parse encrypted image values
                    # TODO: Decrypt using DES
                    # TODO: Save as penguin_decrypted.jpg
                    # TODO: Flash LED
                    # [FIX in TODO]
                    _, payload = message.split(":", 1)
                    enc_chars = [chr(int(x)) for x in payload.split(",") if x]
                    enc_text = "".join(enc_chars)
                    plain_text = des_cipher.decrypt(des_key, enc_text, padding=True, cbc=True)
                    plain_bytes = plain_text.encode("latin-1")
                    with open("penguin_decrypted.jpg", "wb") as f:
                        f.write(plain_bytes)
                    print("[image_server] Decrypted image saved as penguin_decrypted.jpg")
                    flash_led()

                else:
                    print(f"[image_server] Unknown message: {message}")
    except KeyboardInterrupt:
        print("\n[image_server] Shutting down (KeyboardInterrupt).")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        server.close()
        lgpio.gpio_free(h, LED_PIN)
        lgpio.gpiochip_close(h)
        print("[image_server] Closed sockets and cleaned up GPIO.")

if __name__ == "__main__":
    main()
