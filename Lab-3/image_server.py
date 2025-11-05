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

from des import des

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for the LED
LED_PIN = 17

# TODO: Open gpiochip and claim output for the LED
h = lgpio.gpiochip_open(0) 
lgpio.gpio_claim_output(h, LED_PIN, 0)

def flash_led(times=2, duration=0.3):
    """TODO: LED ON/OFF blinking"""
    for i in range(times):
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

                    info = message[4:]
                    e_str, n_str = info.split(",", 1)
                    client_public_key = (int(e_str), int(n_str))
                    print(f"[image_server] Received PUBLIC key: {client_public_key}")

                elif message.startswith("DESKEY:"):
                    # TODO: Decrypt DES key using RSA
                    convert = [int(x) for x in message[7:].split(",") if x]
                    if convert and client_public_key is not NONE:
                       e, n = client_public_key
                       text = ""
                       for c in convert:
                           m = pow(c, e, n)
                           text += chr(m % 256)
                       des_key = text
                    print("[image_server] Recovered DES key.")

                elif message.startswith("IMAGE:"):
                    if des_key is None:
                        print("[image_server] Error: no DES key yet.")
                        continue
                    # TODO: Parse encrypted image values
                    encrypted_image = message[len("IMAGE:"):]
                    # TODO: Decrypt using DES
                    p_text =des().decrypt(encrypted_image, des_key, padding=True, cbc=True)
                    # TODO: Save as penguin_decrypted.jpg
                    with open("penguin_decrypted.jpg", "wb") as f:
                        f.write(p_text)
                    print("[image_server] Decrypted image saved as penguin_decrypted.jpg")

                    # TODO: Flash LED
                    flash_led(0.1)

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


