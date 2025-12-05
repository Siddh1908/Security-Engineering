"""TODO: Make the server more secure against side-channel attacks"""

import socket, time, random
from pathlib import Path



SOCK_PATH = "/tmp/passwordchecker.sock"
Path(SOCK_PATH).unlink(missing_ok=True)

SECRET = b"S3cret!"
DELAY_PER_MATCH = 0.0008 


#
# Random Noise 
# add unpredeictable jitters 
def randomNoise():
    rNoise = random.uniform(0.0005,0.0025)
    time.sleep(rNoise)


# 
# Constant time comparison 
# 

def timeCompare(secret: bytes, candidate: bytes) -> bool:
    #Does the length match?
    if len(secret) != len(candidate):
        # run through to equal out the timing
        fake = 0
        for i in range(len(secret)):
            fake ^= secret[i]
        return False
    result = 0
    for x, y in zip(secret, candidate):
        result |= (x ^ y)
    return result == 0

#
# Timing Padding 
# every request takes at least the timeValue time
# to combat timing signal

timeValue = .003
def padding(secret: bytes, candidate: bytes) -> bool:
    start = time.perf_counter()
    verify = timeCompare(secret, candidate)
    passedTime = time.perf_counter() - start
    leftOver = timeValue - passedTime
    if leftOver > 0:
    	time.sleep(leftOver)
    return verify 



with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.bind(SOCK_PATH)
    s.listen(1)
    print("Listening on:", SOCK_PATH)
    while True:
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            candidate = data.strip()
            ok = padding(SECRET, candidate)
            # Noise
            randomNoise()
            conn.sendall(b"1" if ok else b"0")

