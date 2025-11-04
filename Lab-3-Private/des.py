import random
import math

# ... (all tables remain unchanged)

def string_to_bit_array(text):
    """
    Convert a string into a list of bits.
    Example: 'A' -> [0,1,0,0,0,0,0,1]
    """
    # FIX: Map each char -> 8-bit binary, extend into list[int]
    result = []
    for ch in text:
        b = binvalue(ord(ch), 8)
        result.extend(int(bit) for bit in b)
    return result

def bit_array_to_string(array):
    """
    Convert a list of bits into a string.
    Example: [0,1,0,0,0,0,0,1] -> 'A'
    """
    # FIX: Group by 8, then convert to chars
    chars = []
    for byte in nsplit(array, 8):
        val = int("".join(str(b) for b in byte), 2)
        chars.append(chr(val))
    return "".join(chars)

def binvalue(val, bitsize):
    binval = bin(val)[2:]
    while len(binval) < bitsize:
        binval = "0" + binval
    return binval

def nsplit(s, n):
    return [s[k:k+n] for k in range(0, len(s), n)]

ENCRYPT=1
DECRYPT=0

class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()
        
    # ... run and run_cbc unchanged ...

    def substitute(self, d_e):
        subblocks = nsplit(d_e, 6)
        result = []
        for i, subblock in enumerate(subblocks):
            s_box_out = self.compute_s_box(subblock, round=i)  # returns '####' string
            result.extend(int(bit) for bit in s_box_out)
        return result
                
    def permut(self, block, table):
        return [block[x-1] for x in table]
    
    def expand(self, block, table):
        return [block[x-1] for x in table]
    
    def xor(self, t1, t2):
        """
        Apply bitwise XOR between two lists of bits.
        """
        # FIX: element-wise XOR
        return [a ^ b for a, b in zip(t1, t2)]

    def generatekeys(self):
        """
        Generate 16 round keys from the initial key.
        """
        # FIX: full DES key schedule
        self.keys = []
        key_bits_64 = string_to_bit_array(self.password)   # 64 bits
        key56 = self.permut(key_bits_64, CP_1)            # 56 bits
        g, d = nsplit(key56, 28)                          # two 28-bit halves
        for shift in SHIFT:
            g, d = self.shift(g, d, shift)                # left-rotate halves
            joined = g + d                                # 56 bits
            subkey = self.permut(joined, CP_2)            # 48 bits
            self.keys.append(subkey)

    def shift(self, g, d, n):
        return g[n:] + g[:n], d[n:] + d[:n]
    
    def addPadding(self):
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)
    
    def removePadding(self, data):
        pad_len = ord(data[-1])
        return data[:-pad_len]
    
    def encrypt(self, key, text, padding=False,cbc=False,IV='ASASASAS'):
        if cbc:
            return self.run_cbc(key, text, ENCRYPT, padding,IV)
        else:
            return self.run(key, text, ENCRYPT, padding)
    
    def decrypt(self, key, text, padding=False,cbc=False,IV='ASASASAS'):
        if cbc:
            return self.run_cbc(key, text, DECRYPT, padding,IV)
        else:
            return self.run(key, text, DECRYPT, padding)

    def compute_s_box(self, block, round):
        """
        Compute S-Box substitution for a 6-bit block.
        Input: block (list of 6 bits), round (0..7)
        Output: list of 4 bits
        """
        # FIX: S-box lookup (row from bits 0 & 5, col from bits 1..4)
        b = block
        row = (b[0] << 1) | b[5]
        col = (b[1] << 3) | (b[2] << 2) | (b[3] << 1) | b[4]
        val = S_BOX[round][row][col]
        return binvalue(val, 4)  # as '####' string
