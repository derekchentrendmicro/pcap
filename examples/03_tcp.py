import sys
import time
import struct

pcap_hdr = 'd4c3b2a10200040000000000000000000020000001000000'.decode('hex')
syn = '021ac5180000021ac51200000800450000388ebd4000200621250a018dab0a0b0927a074018522e3499600000000900216a02a650000020405b40101080a7237f28100000000'.decode('hex')
synack = '021ac5120000021ac5180000080045000038b08140002006ff600a0b09270a018dab0185a0743e6a458222e34997901216a0404f0000020405b40101080a7237f3e07237f281'.decode('hex')
ack = '021ac5180000021ac51200000800450000348ebc40002006212a0a018dab0a0b0927a074018522e349973e6a4583801016a055c600000101080a7237f4c77237f3e0'.decode('hex')


with open(sys.argv[2],'wb') as f:
  f.write(pcap_hdr)
  t0 = time.time()
  for p in syn,synack:
    plen = len(p)
    hdr = struct.pack('<QII',0,plen,plen)
    f.write(hdr + p)
  with open(sys.argv[1]) as g:
    buf = g.read(100)
    seq, = struct.unpack('>I',ack[38:42]) # seq: 0x26 
    ack_ip_len, = struct.unpack('>H',ack[16:18])
    while buf:
      buf_len = len(buf)
      ip_len = ack_ip_len + buf_len 
      plen = len(ack) + buf_len
      hdr = struct.pack('<QII',0,plen,plen)
      f.write(hdr)
      ack = ack[0:16] + struct.pack('>H',ip_len) + ack[18:38] + struct.pack('>I',seq) + ack[42:] # ip: 0x10, seq: 0x26
      f.write(ack + buf)
      seq += buf_len
      buf = g.read(100)
  t1 = time.time()
print sys.argv[0]+ ": " + str(t1-t0) + "s"

