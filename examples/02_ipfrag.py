import sys
import time
import struct

def ip_frag(f_in,f_out):
    with open(f_in,'rb') as f:
     with open(f_out,'wb') as g:
      g.write(f.read(24))
      hdr = f.read(16)
      t0 = time.time()
      n=1
      frag = [{},{}]
      while hdr:
        ts,caplen,actlen = struct.unpack('<QII',hdr)
        pkt = f.read(caplen)

        ip_len, = struct.unpack('>H',pkt[16:18])
        ip_payload_len = ip_len - 20
        if n%10 == 0 and ip_payload_len > 16:
           frag[0]['len'] = 16
           frag[1]['len']= ip_payload_len - frag[0]['len']
           frag[0]['hdr'] = pkt[0:16] + struct.pack('>H',20+frag[0]['len']) + pkt[18:20] + struct.pack('>H',0x2000) + pkt[22:34] # more frag bit
           frag[1]['hdr'] = pkt[0:16] + struct.pack('>H',20+frag[1]['len']) + pkt[18:20] + struct.pack('>H',0x0002) + pkt[22:34] # frag offset = 2*8 = 16
           frag[0]['payload'] = pkt[34:50] # 16 bytes 
           frag[1]['payload'] = pkt[50:]   # remaining
           for i in xrange(2):
             pkt_new = frag[i]['hdr'] + frag[i]['payload']
             caplen = struct.pack('<I',len(pkt_new))
             hdr_new = hdr[0:8] + caplen + caplen 
             g.write(hdr_new)
             g.write(pkt_new)
        else:
           g.write(hdr)
           g.write(pkt)
        hdr = f.read(16)
        n += 1
      t1 = time.time()
    print sys.argv[0]+ ": " + str(t1-t0) + "s"

ip_frag(sys.argv[1],sys.argv[2])
 
