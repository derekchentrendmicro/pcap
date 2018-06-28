import sys
import time
import struct

def raw_io(f_in,f_out):
    with open(f_in,'rb') as f:
     with open(f_out,'wb') as g:
      g.write(f.read(24))
      hdr = f.read(16)
      while hdr:
        g.write(hdr)
        ts,caplen,actlen = struct.unpack('<QII',hdr)
        pkt = f.read(caplen)
        g.write(pkt)
        hdr = f.read(16)

t0 = time.time()
raw_io(sys.argv[1],sys.argv[2])
t1 = time.time()
print sys.argv[0]+ ": " + str(t1-t0) + "s"
