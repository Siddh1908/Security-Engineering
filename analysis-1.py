"""
Lab 4 - Part 3: PRNG vs TRNG Comparative Analysis
Platform: Raspberry Pi 5 (Python 3.11)

This script compares:
    - PRNG (LFSR-based pseudorandom generator)
    - TRNG (hardware jitter-based true random generator)

Outputs:
    - Entropy values for both
    - Histograms, autocorrelation plots
    - LED + buzzer feedback for higher entropy source
"""
#from lfsr_prng import lfsr
#from trng import trng
import lgpio
import time
import math
import matplotlib.pyplot as plt
import numpy as np

# ---------------- GPIO CONFIG ----------------
PIN_LED = 27
PIN_BUZZER = 18
PIN_INPUT = 17  # For TRNG input

chip = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(chip, PIN_LED)
lgpio.gpio_claim_output(chip, PIN_BUZZER)
lgpio.gpio_claim_input(chip, PIN_INPUT)

# ---------------- UTILITIES ----------------
def beep(duration=0.1):
    lgpio.gpio_write(chip, PIN_BUZZER, 1)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_BUZZER, 0)

def blink_led(bit=1, duration=0.05):
    lgpio.gpio_write(chip, PIN_LED, bit)
    time.sleep(duration)
    lgpio.gpio_write(chip, PIN_LED, 0)

def trng(bits = 512):
    """Redfine your trng function from trng.py here"""
    output_bits = []
    previous_t = time.time_ns()
    while len(output_bits) < bits:
      while lgpio.gpio_read(chip, PIN_INPUT) == 0:
        pass
      current_t = time.time_ns()
      delta = current_t - previous_t
      bit = delta & 1
      output_bits.append(bit)
      blink_led(bit)
    return output_bits
def lfsr(seed = 0b100111,taps =(5,4), n_bits = 6, n_values = 512):
    """Redefine your lfsr function from lfsr_prng.py"""
    if seed ==0:
      seed = 1
    reg = seed
    output_bits = []
    for _ in range(n_values):
      output_bits.append(reg & 1)
      new_bit = 0
      for t in taps:
        new_bit ^= (reg >> (t-1)) & 1
      reg = (reg >> 1) | (new_bit << (n_bits - 1))
    return output_bits

def entropy(data):
    """Shannon entropy (bits per symbol)."""
    """TODO"""
    arrayy = np.array(data, dtype = float)
    nump = len(arrayy)
    p1 = np.sum(arrayy)/nump
    p0 = 1.0 - p1
    h = 0.0
    if p0 > 0.0:
      h -= p0 * math.log2(p0)
    if p1 > 0.0:
      h -= p1 * math.log2(p1)
    return h


def autocorrelation(bits):
    """ Compute lag-1 autocorrection coefficient"""
    "TODO"
    arrayy = np.array(bits, dtype = float)
    nump = len(arrayy)
    if nump<2:
      return 0.0
    mean = np.mean(arrayy)
    xi = arrayy[:-1] - mean
    x2 = arrayy[1:] - mean
    num = np.sum(xi*x2)
    den = np.sum((arrayy - mean) ** 2)
    return num/den


def plot_comparison(prng_bits, trng_bits, H_prng, H_trng):
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(prng_bits, bins=2, color='skyblue', edgecolor='black')
    plt.title(f"Write a title here={H_prng:.3f}")
    plt.xticks([0, 1])
    plt.xlabel("Write the x label here")
    plt.ylabel("Write the y label here")

    plt.subplot(1, 2, 2)
    plt.hist(trng_bits, bins=2, color='orange', edgecolor='black')
    plt.title(f"Write a title here={H_trng:.3f}")
    plt.xticks([0, 1])
    plt.xlabel("Write the x label here")
    plt.ylabel("Write the x label here")

    plt.tight_layout()
    plt.show()

# ---------------- MAIN ----------------
def main():
    print("Collecting data from both generators...\n")

    prng_bits = lfsr()
    trng_bits = trng()

    H_prng = entropy(prng_bits)
    H_trng = entropy(trng_bits)
    R_prng = autocorrelation(prng_bits)
    R_trng = autocorrelation(trng_bits)

    print(f"PRNG Entropy = {H_prng:.3f} bits/bit,  Autocorr = {R_prng:.3f}")
    print(f"TRNG Entropy = {H_trng:.3f} bits/bit,  Autocorr = {R_trng:.3f}\n")

    plot_comparison(prng_bits, trng_bits, H_prng, H_trng)

    if H_trng > H_prng:
        print("TRNG shows higher entropy — more random.")
        blink_led(1)
        beep(0.2)
    else:
        print("PRNG appears more uniform in this run.")
        for _ in range(2):
            blink_led(1)
            time.sleep(0.1)
            blink_led(0)

    lgpio.gpiochip_close(chip)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lgpio.gpiochip_close(chip)
        print("\nInterrupted — GPIO cleaned up.")
