# coding=utf-8


import os
import sys

from socket import AF_INET
from socket import SOCK_RAW
from socket import IPPROTO_RAW
from socket import socket
from socket import inet_ntop
from socket import inet_pton
from socket import ntohs
from socket import htons
from socket import ntohl
from socket import htonl
from socket import IPPROTO_TCP
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR

from ctypes import BigEndianStructure
from ctypes import c_uint32
from ctypes import c_uint16
from ctypes import c_uint8
from ctypes import c_uint64
from ctypes import sizeof

from struct import unpack as st_unpack
from struct import pack as st_pack

from binascii import unhexlify
from binascii import hexlify

from dpkt import Packet
from dpkt.ip import IP
from dpkt.tcp import TCP
from dpkt.dpkt import in_cksum

import subprocess
from time import sleep


def inet_p2nb(p):
    nb = inet_pton(AF_INET, p)
    return nb
def inet_nb2p(nb):
    return inet_ntop(AF_INET, nb)

def inet_p2n(p):
    n = inet_pton(AF_INET, p)
    n = st_unpack("I",n)[0]
    return n

def inet_n2p(n):
    n = st_pack("I",n)
    p = inet_ntop(AF_INET, n)
    return p

def inet_nb2h(nb):
    p = inet_nb2p(nb)
    n = inet_p2n(p)
    return ntohl(n)

def inet_nb2n(nb):
    p = inet_nb2p(nb)
    n = inet_p2n(p)
    return n


class BaseSt(BigEndianStructure):
    def pack(self):
        return buffer(self)[:]

    @classmethod
    def unpack(cls, hexStream):
        a = unhexlify(hexStream)
        b = cls.from_buffer_copy(a)
        restBytes = a[sizeof(b)::]
        return b, hexlify(restBytes)

class Ipv4PseudoHdr(BaseSt):
    _pack_=1
    _fields_=[
        ('src_addr', c_uint32),
        ('dst_addr', c_uint32),
        ('rsv', c_uint8),
        ('protocol', c_uint8),
        ('protocol_size', c_uint16)
    ]


class TOA(BaseSt):
    _pack_ = 1
    _fields_ = [
        ('opcode', c_uint8),
        ('opsize', c_uint8),
        ('port', c_uint16),
        ('ip', c_uint32),
    ]


def add_toa(ip, tcp):
    toa = TOA()
    toa.opcode = 254
    toa.opsize = 8
    toa.port = 23
    toa.ip = ntohl(inet_p2n("100.101.102.103"))
    tcp.opts = tcp.opts + toa.pack()
    tcp.off = tcp.off + 2

    ip.len = ip.len + 8


def tcp_handshake_syn(sk, src_addr, dst_addr, seq):
    syn_pkt = ("4500003c9fa5400040069d147f0000017f00000198f40d3d1dbce"
               "96a00000000a002aaaafe3000000204ffd70402080a3e4876cf0000000001030307")
    syn_pkt = unhexlify(syn_pkt)

    ip = IP(syn_pkt)
    ip.src = inet_p2nb(src_addr[0])
    ip.dst = inet_p2nb(dst_addr[0])

    tcp = ip.data
    tcp.sport = src_addr[1]
    tcp.dport = dst_addr[1]
    tcp.seq = seq

    # add_toa(ip, tcp)

    tcp.sum = 0
    ip_pseudo_hdr = Ipv4PseudoHdr()
    ip_pseudo_hdr.src_addr = inet_nb2h(ip.src)
    ip_pseudo_hdr.dst_addr = inet_nb2h(ip.dst)
    ip_pseudo_hdr.protocol = IPPROTO_TCP
    ip_pseudo_hdr.protocol_size = len(tcp)
    tcp.sum = in_cksum(ip_pseudo_hdr.pack() + tcp.pack())

    syn_tcp_pkt = tcp.pack()
    r = sk.sendto(syn_tcp_pkt, (dst_addr[0],0))
    print("syn {} return {}".format(hexlify(syn_tcp_pkt), r))

def tcp_handshake_ack(sk, src_addr, dst_addr, seq, ack_seq):
    ack_pkt = ("45000034da9740004006622a7f0000017f000001c64c0d"
               "3db68d5e7dbfe29d6780100156fe2800000101080a468d84ea468d84ea")

    ack_pkt = unhexlify(ack_pkt)
    ip = IP(ack_pkt)
    ip.src = inet_p2nb(src_addr[0])
    ip.dst = inet_p2nb(dst_addr[0])

    tcp = ip.data
    tcp.sport = src_addr[1]
    tcp.dport = dst_addr[1]
    tcp.seq = seq
    tcp.ack = ack_seq

    add_toa(ip, tcp)

    tcp.sum = 0
    ip_pseudo_hdr = Ipv4PseudoHdr()
    ip_pseudo_hdr.src_addr = inet_nb2h(ip.src)
    ip_pseudo_hdr.dst_addr = inet_nb2h(ip.dst)
    ip_pseudo_hdr.protocol = IPPROTO_TCP
    ip_pseudo_hdr.protocol_size = len(tcp)
    tcp.sum = in_cksum(ip_pseudo_hdr.pack() + tcp.pack())

    ack_tcp_pkt = tcp.pack()
    r = sk.sendto(ack_tcp_pkt, (dst_addr[0], 0))
    print("ack {} return {}".format(hexlify(ack_tcp_pkt), r))

def tcp_handshake_close(sk, src_addr, dst_addr, seq, ack_seq):
    # rst pkt will exception socket.error: [Errno 1] Operation not permitted

    fin_pkt=("450000349b2140004006a1a07f0000017f000001c7c20d3db204a0efb0"
             "cf0b0180110156fe2800000101080a46cf3bf546cf3bf5")
    fin_pkt = unhexlify(fin_pkt)
    ip = IP(fin_pkt)
    ip.src = inet_p2nb(src_addr[0])
    ip.dst = inet_p2nb(dst_addr[0])

    tcp = ip.data
    tcp.sport = src_addr[1]
    tcp.dport = dst_addr[1]
    tcp.seq = seq
    tcp.ack = ack_seq
    tcp.sum = 0
    ip_pseudo_hdr = Ipv4PseudoHdr()
    ip_pseudo_hdr.src_addr = inet_nb2h(ip.src)
    ip_pseudo_hdr.dst_addr = inet_nb2h(ip.dst)
    ip_pseudo_hdr.protocol = IPPROTO_TCP
    ip_pseudo_hdr.protocol_size = len(tcp)
    tcp.sum = in_cksum(ip_pseudo_hdr.pack() + tcp.pack())

    fin_tcp_pkt = tcp.pack()
    r = sk.sendto(fin_tcp_pkt, (dst_addr[0], 0))
    print("fin {} return {}".format(hexlify(fin_tcp_pkt), r))

def tcp_handshake(sk, src_addr, dst_addr, seq):

    tcp_handshake_syn(sk, src_addr, dst_addr, seq)

    subprocess.call("iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP", shell=True)
    try:
        # recv syn+ack
        src_ipn = inet_p2n(src_addr[0])
        while True:
            ip_pkt,addr = sk.recvfrom(128*1024)
            ip = IP(ip_pkt)
            if ip.p != IPPROTO_TCP:
                print("syn+ack invalid not tcp {}".format(hexlify(ip_pkt)))
            else:
                tcp = ip.data
                if not(inet_nb2n(ip.dst) == src_ipn and tcp.dport == src_addr[1]
                    and tcp.ack == (seq+1)):
                    print("syn+ack invalid not our tcp pkt {}".format(hexlify(ip_pkt)))
                else:
                    print("syn+ack valid {}".format(hexlify(ip_pkt)))
                    ack_seq = tcp.seq + 1
                    tcp_handshake_ack(sk, src_addr, dst_addr, seq+1, ack_seq)
                    tcp_handshake_close(sk, src_addr, dst_addr, seq + 1, ack_seq)
                    break
    finally:
        pass
        sleep(1)
        subprocess.call("iptables -L OUTPUT -n --line-numbers", shell=True)
        subprocess.call("iptables -D OUTPUT 1", shell=True)

    print("done tcp handshake")


def main():
    import random

    sk = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
    raddr = ("127.0.0.1", 3388)
    laddr = ("127.0.0.1", random.randint(1024,65535))
    seq = 0x12345675

    print("{} -> {}".format(laddr, raddr))

    # use tcp socket bind laddr, so not response RST when recv syn+ack
    # https://stackoverflow.com/questions/48891727/using-socket-af-packet-sock-raw-but-tell-kernel-to-not-send-rst
    # iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

    # the fake socket not work
    # sk0 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    # sk0.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # sk0.bind(laddr)


    # nothing
    # r = sk.bind(laddr)
    # print("bind {} return {}".format(laddr,r))


    tcp_handshake(sk, laddr, raddr, seq)



if __name__ == '__main__':
    main()

