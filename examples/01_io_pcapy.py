import sys
import time
import pcapy

def pcapy_io(f_in,f_out):

    pt = pcapy.open_offline(f_in)
    pd = pt.dump_open(f_out)
    hdr, body = pt.next()
    while hdr is not None:
        pd.dump(hdr, body)
        hdr, body = pt.next()
    del pd
    pt.close()

t0 = time.time()
pcapy_io(sys.argv[1], sys.argv[2])
t1 = time.time()
print sys.argv[0] + ": " + str(t1-t0) + "s"


