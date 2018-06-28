import dpkt
import sys
import time

def dpkt_io(f_in,f_out):
    f = open(f_in,'rb')
    g = open(f_out,'wb')
    pcap_in = dpkt.pcap.Reader(f)
    pcap_out = dpkt.pcap.Writer(g)
    for ts, buf in pcap_in:
        pcap_out.writepkt(buf,ts)
    f.close()
    g.close()

t0 = time.time()
dpkt_io(sys.argv[1],sys.argv[2])
t1 = time.time()
print sys.argv[0] + ": " + str(t1-t0) + "s"
