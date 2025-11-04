import socket
import time
import lgpio

from des import des

# --- GPIO Setup (TODO: complete this section) ---
# FIX: choose LED pin and claim output
LED_PIN = 23
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 0, LED_PIN, 0)

def flash_led(times=2, duration=0.3):
    """TODO: LED ON/OFF blinking"""
    # FIX:
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
                    # FIX:
                    _, key_str = message.split(":", 1)
                    e_str, n_str = key_str.split(",", 1)
                    client_public_key = (int(e_str), int(n_str))
                    print(f"[image_server] Received client PUBLIC key: {client_public_key}")

                elif message.startswith("DESKEY:"):
                    # TODO: Decrypt DES key using RSA
                    # Per scaffold: client "encrypted" with PRIVATE; we "decrypt" with PUBLIC (e,n)
                    # FIX:
                    if client_public_key is None:
                        print("[image_server] Error: no public key yet.")
                        continue
                    e, n = client_public_key
                    key_payload = message[len("DESKEY:"):]
                    cipher_vals = [int(x) for x in key_payload.split(",") if x]
                    recovered = "".join(chr(pow(c, e, n)) for c in cipher_vals)
                    des_key = recovered
                    print(f"[image_server] Recovered DES key: {repr(des_key)}")

                elif message.startswith("IMAGE:"):
                    if des_key is None:
                        print("[image_server] Error: no DES key yet.")
                        continue
                    # TODO: Parse encrypted image values
                    # FIX:
                    img_payload = message[len("IMAGE:"):]
                    enc_img_vals = [int(x) for x in img_payload.split(",") if x]
                    enc_img_text = "".join(chr(v) for v in enc_img_vals)

                    # TODO: Decrypt using DES
                    # FIX:
                    cipher = des()
                    dec_text = cipher.decrypt(des_key, enc_img_text, padding=True, cbc=True, IV='ASASASAS')

                    # TODO: Save as penguin_decrypted.jpg
                    # FIX: dec_text is a Latin-1 string → bytes
                    dec_bytes = dec_text.encode("latin-1")
                    with open("penguin_decrypted.jpg", "wb") as f:
                        f.write(dec_bytes)
                    print("[image_server] Wrote penguin_decrypted.jpg")

                    # TODO: Flash LED
                    # FIX:
                    flash_led(times=3, duration=0.15)

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
