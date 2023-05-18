# Import numpy and numpysocket for data manipulation and transfer
import numpy as np
from numpysocket import NumpySocket as nps

# Import time and datetime for timekeeping and logging
import time
from datetime import datetime as dt

def slient_listener():
    with nps() as n:
        n.connect(('', 8080))
        
        while True:
            if n.recv() == b'1':
                n.disconnect()
                main()
                break
            
def main():
    with nps() as n:
        n.connect(('', 8080))
        while True:
            data = np.zeros((320, 240, 3), dtype=np.uint8)
            data[:] = (0, 0, 255)
            n.sendall(data)
            if n.recv() == b'0':
                break
            
if __name__ == '__main__':
    slient_listener()