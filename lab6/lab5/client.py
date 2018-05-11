from check import ip_checksum
import threading
import socket 
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;

base = 0
nextseqnum = 0
maxseqnum = 7
windowsize = 4
iscorrupt = 1

def makepkt(num, data):
    global iscorrupt
    if iscorrupt == 1 and data == 2:
        iscorrupt = 0
        checksum = 'corrupted'
        print "packet " + str(data) + "is corrupted, sending "
    else:
        checksum = ip_checksum(str(data))

    packet = str(num) + str(data) + checksum
    return packet

def timerStart(base, windowSize):
    global timer
    global nextseqnum
    timer = threading.Timer(2, timerStart, [base, windowSize])
    timer.start()
    print
    for i in range(base, base + windowSize):
        if i <= maxseqnum:
            sndpkt = makepkt(i,i)
            s.sendto(sndpkt, (host,port))
            nextseqnum = i + 1
            print 'packet' + str(i) + ' sent'

def reset():
    global base
    global nexseqnum
    if base > maxseqnum:
        base = 0
        nextseqnum = 0


while 1:
    msg = raw_input("Press anykey to send packets")
    try:
        reset()
        for i in range(2):
            if base == nextseqnum:
                timerStart(base, windowsize)

            while 1:
                d = s.recvfrom(1024)
                reply = d[0]
                ACK = int(reply[0])
                ACKCheckSum = reply[1:]
                CheckSum = ip_checksum(str(ACK))

                if ACKCheckSum == CheckSum:
                    base = ACK + 1
                    if base == nextseqnum:
                        timer.cancel()
                        break
                    else:
                        timer.cancel()
                        timer = threading.Timer(2,timerStart, [base, windowsize])
                        timer.start()
        
    except socket.error, msg:
        print 'Error code: ' + str(msg[0]) + 'Message ' + msg[1]
        sys.exit()
    

