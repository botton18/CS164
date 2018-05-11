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
while 1:
    if seq > 7:
        seq = 0
    d = s.recvfrom(1024)
    toconcat = d[0]
    addr = d[1]   
    if not toconcat:
        break

    senderseq = int(toconcat[0])
    sendermsg = int(toconcat[1])
    senderchecksum = toconcat[2:]
    
    print 'SEQNUM ' + str(senderseq) + '\n'
    #reply = 'OK...' + data
    checksum = ip_checksum(str(sendermsg))
    if checksum == senderchecksum:
        if senderseq == seq:
            print 'Received ' + str(senderseq)
            print 'Send ' + str(seq)
            sndpkt = makepacket(seq)
            seq = seq + 1
        else:
            print 'Received ' + str(senderseq)
            print 'Send ' + str(seq)
            sndpkt = makepacket(seq - 1)
    else:
        print 'checksum != senderchecksum'
        print 'Received ' + str(senderseq)
        print 'Send ' + str(seq - 1)
        sndpkt = makepacket(seq-1)

    s.sendto(sndpkt,addr)
s.close()
