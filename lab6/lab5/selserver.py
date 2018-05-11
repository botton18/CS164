from check import ip_checksum
import socket
import sys
import threading
HOST = ''
PORT = 8888

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket Created'

except socket.error, msg:
    print 'Failed to create socket'
    sys.exit()


try:
    s.bind((HOST,PORT))
except socket.error,msg:
    print 'Bind fail'
    sys.exit()
print 'Socket bind complete'

def makepacket(num):
    chksum = ip_checksum(str(num))
    packet = str(num) + chksum
    return packet

seq = 0
count = 0
windowsize = 4
maxseqnum = 8
base = 0
while 1:
    d = s.recvfrom(1024)
    recv = d[0]
    address = d[1]

    seqnum = int(recv[0])
    data = int(recv[1])
    checksum = recv[2:]
    Check = ip_checksum(str(data))

    if checksum == Check:
        if seqnum > base and seqnum >= base + windowsize:
            base = seqnum
        if seqnum < base:
            print 'Received: ' + str(seqnum)
            sndpkt = makepacket(seqnum)
        if seqnum > base and seqnum < base + windowsize:
            print 'Received: ' + str(seqnum)
            sndpkt = makepacket(seqnum)
        if seqnum == base:
            print 'Received: ' + str(seqnum)
            sndpkt = makepacket(seqnum)
            base = base + 1

        s.sendto(sndpkt, address)
        print 'ACK' + str(seqnum) + 'send'

        if base == maxseqnum:
            base = 0

    else:
        print 'Corrupted packet ' + str(seqnum) 
s.close()
