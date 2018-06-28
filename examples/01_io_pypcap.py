import sys
import time
import pcap

def pypcap_io(f_in,f_out):

    pt = pcap.pcap(f_in)
    pd = pcap.pcap(f_out,dump=True)
    for ts,pkt in pt:
       pd.dump(pkt)

t0 = time.time()
pypcap_io(sys.argv[1], sys.argv[2])
t1 = time.time()
print sys.argv[0] + ": " + str(t1-t0) + "s"


