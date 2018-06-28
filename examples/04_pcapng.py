import sys
import struct

with open(sys.argv[1],'rb') as f:
 with open(sys.argv[2],'wb') as g:
  i=1
  hdr = f.read(8)
  while hdr:
    type,size = struct.unpack('<II',hdr)
    size -= 8
    if type == 6:
       pkthdr = f.read(20)
       iid,ts,caplen,actlen = struct.unpack('<IQII',pkthdr)
       pkt = f.read(caplen)
       size -= (20+caplen)
       if i > 2578865 and i < 2578950:
          g.write(hdr)
          g.write(pkthdr)
          g.write(pkt)
          g.write(f.read(size))
       else:
          f.read(size)
       i += 1
    else:
       g.write(hdr)
       g.write(f.read(size))
    hdr = f.read(8)


