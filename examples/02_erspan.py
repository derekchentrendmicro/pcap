import sys
import time
import struct

def to_erspan(f_in,f_out):
    erspan = '000c29f51cdf6805ca1036f50800450000663fd00000402f3d3d0a00754a0a0074102000655802000000'
    erspan = erspan.decode('hex')
    with open(f_in,'rb') as f:
     with open(f_out,'wb') as g:
      g.write(f.read(24))
      hdr = f.read(16)
      t0 = time.time()
      while hdr:
        ts,caplen,actlen = struct.unpack('<QII',hdr)
        pkt = f.read(caplen)

        caplen += len(erspan)
        ip_len = caplen - 14
        erspan_new = erspan[0:16] + struct.pack('>H',ip_len) + erspan[18:]
        caplen = struct.pack('<I',caplen)
        hdr_new = hdr[0:8] + caplen + caplen
        pkt_new = erspan_new + pkt

        g.write(hdr_new)
        g.write(pkt_new)

        hdr = f.read(16)
      t1 = time.time()
    print sys.argv[0]+ ": " + str(t1-t0) + "s"

to_erspan(sys.argv[1],sys.argv[2])





