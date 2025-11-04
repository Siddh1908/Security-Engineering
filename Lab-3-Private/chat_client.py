import socket
import time
import lgpio
from RSA import generate_keypair, encrypt

# --- GPIO Setup (TODO: complete this section) ---
# FIX: choose buzzer pin and claim output
BUZZER_PIN = 18  # BCM pin for active buzzer (change if you wired differently)
h = lgpio.gpiochip_open(0)  # FIX: open gpiochip0
lgpio.gpio_claim_output(h, 0, BUZZER_PIN, 0)  # FIX: claim output, start LOW

def buzz(duration=0.3):
    """TODO: Make the buzzer turn ON, sleep, then OFF."""
    # FIX: simple on/off pulse
    lgpio.gpio_write(h, BUZZER_PIN, 1)
    time.sleep(duration)
    lgpio.gpio_write(h, BUZZER_PIN, 0)

# --- RSA setup (use your primes from prime_numbers.xlsx) ---
p, q = 3557, 2579
public, private = generate_keypair(p, q)  # (e, n), (d, n)

# --- Socket setup ---
HOST = "127.0.0.1"   # Change to server IP if needed
PORT = 5000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[chat_client] Connected to {HOST}:{PORT}")

    # Step 1: Send PUBLIC key to server
    e, n = public
    key_msg = f"KEY:{e},{n}"
    client.sendall(key_msg.encode("utf-8"))
    print(f"[chat_client] Sent public key: (e={e}, n={n})")

    # Step 2: Loop for sending encrypted messages
    while True:
        msg = input("Enter message (or 'exit'): ")
        if msg.lower() == "exit":
            break

        # TODO: Encrypt msg with RSA
        # NOTE: The server stores our PUBLIC key and "decrypts" with it.
        # That means here we must "encrypt" with our PRIVATE key (signature-style),
        # so the server can recover with our public key in this scaffold.
        # FIX:
        cipher_list = encrypt(private, msg)

        # TODO: Convert cipher list -> comma string
        # FIX:
        cipher_str = ",".join(map(str, cipher_list))

        # TODO: Send ciphertext to server
        # FIX:
        package = f"CIPHER:{cipher_str}"
        client.sendall(package.encode("utf-8"))

        # TODO: Buzz
        # FIX:
        buzz()
        print("[chat_client] Sent encrypted message and buzzed.")

    client.close()
    lgpio.gpio_free(h, BUZZER_PIN)
    lgpio.gpiochip_close(h)
    print("[chat_client] Closed connection and cleaned up GPIO.")

if __name__ == "__main__":
    main()
