'''
reference: https://github.com/public0821/libpcapy
'''

from ctypes import *
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

lib=CDLL('/usr/lib/x86_64-linux-gnu/libpcap.so')
lib.pcap_open_dead.restype = pcap_t_p
lib.pcap_dump_open.restype = pcap_dumper_t_p
lib.pcap_next.restype = c_ubyte_p
lib.pcap_open_offline.restype = pcap_t_p

errbuf = create_string_buffer(256)
pt=lib.pcap_open_offline('test.pcap',errbuf)

hdr=pcap_pkthdr()
pkt=lib.pcap_next(pt,byref(hdr))
string_at(pkt, hdr.caplen)

pdt=lib.pcap_open_dead(1,65535)
pd=lib.pcap_dump_open(pdt,'pktdump.cap')
lib.pcap_dump(pd,byref(hdr),pkt)

lib.pcap_dump_close(pd)
lib.pcap_close(pt)
lib.pcap_close(pdt)
