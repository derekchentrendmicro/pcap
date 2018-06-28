import time
import sys
from scapy.all import PcapReader,PcapWriter

def scapy_io(f_in,f_out):
    f = PcapReader(f_in)
    o = PcapWriter(f_out)
    pkt = f.read_packet()
    while pkt is not None:
        o.write(pkt)
        pkt = f.read_packet()
    f.close()
    o.close()

t0 = time.time()
scapy_io(sys.argv[1],sys.argv[2])
t1 = time.time()
print sys.argv[0] + ": " + str(t1-t0) + "s"
