from ctypes import *
import sys
import time

class timeval(Structure):
    _fields_ = [("tv_sec", c_long),
                ("tv_usec", c_long)]

class pcap_pkthdr(Structure):
    _fields_ = [("ts", timeval),
                ("caplen", c_uint32),
                ("len", c_uint32)]

class pcap_t(Structure):
    pass

class pcap_dumper_t(Structure):
    pass

pcap_t_p = POINTER(pcap_t)
pcap_dumper_t_p = POINTER(pcap_dumper_t)
pcap_pkthdr_p = POINTER(pcap_pkthdr)
c_ubyte_p = POINTER(c_ubyte)

lpcap = CDLL('/usr/lib64/libpcap.so')
lpcap.pcap_open_dead.restype = pcap_t_p
lpcap.pcap_dump_open.restype = pcap_dumper_t_p
lpcap.pcap_next.restype = c_ubyte_p
lpcap.pcap_open_offline.restype = pcap_t_p

errbuf = create_string_buffer(256)
pt = lpcap.pcap_open_offline(sys.argv[1],errbuf)
pdt = lpcap.pcap_open_dead(1,65535)
pd = lpcap.pcap_dump_open(pdt,sys.argv[2])

t0 = time.time()

hdr = pcap_pkthdr()
pkt = lpcap.pcap_next(pt,byref(hdr)) # check pkt by string_at(pkt, hdr.caplen)
while pkt:
    lpcap.pcap_dump(pd,byref(hdr),pkt)
    pkt = lpcap.pcap_next(pt,byref(hdr))

lpcap.pcap_dump_close(pd)
lpcap.pcap_close(pt)
lpcap.pcap_close(pdt)

t1 = time.time()
print sys.argv[0] + ": " + str(t1-t0) + "s"
