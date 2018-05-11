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
maxseqnum = 8
windowsize = 4
iscorrupt = 1
NACK = -1
def makepkt(num, data):
    global iscorrupt
    if iscorrupt == 1 and data == 1:
        iscorrupt = 0
        checksum = 'corrupted'
    else:
        checksum = ip_checksum(str(data))

    packet = str(num) + str(data) + checksum
    return packet

def timerStart(seqnum, thelist, index):
    thelist[index] = threading.Timer(2, timerStart, [seqnum, thelist, index])
    thelist[index].start()
    packet = makepkt(seqnum, seqnum)
    s.sendto(packet,(host,port))
    print 'Seq num: ' + str(seqnum)
def reset():
    global base
    global nexseqnum
    base = 0
    nextseqnum = 0

def getbase(acklist, base, windowsize):
    global NACK
    for i in range(base, base + windowsize):
        if acklist[i] == NACK:
            return i
    newbase = base + windowsize
    return newbase

while 1:
    msg = raw_input('press enter to send')
    try:
        reset()
        thelist = [None] * 10000
        acklist = [NACK] * maxseqnum
        for i in range(base, base + windowsize):
            timerStart(nextseqnum, thelist, i)
            nextseqnum = nextseqnum + 1
        
        while 1:
            d = s.recvfrom(1024)
            reply = d[0]
            Num = int(reply[0])
            check = (reply[1:])
            CheckSum = ip_checksum(str(Num))
            print 'received ack' + str(Num)
            if CheckSum == check:
                acklist[Num] = Num
                index = Num
                thelist[index].cancel()
                
                if base == maxseqnum - 1:
                    break

                if base == Num and nextseqnum < maxseqnum:
                    index = nextseqnum
                    timerStart(nextseqnum, thelist, index)
                    nextseqnum = nextseqnum + 1
                    base = getbase(acklist, base, windowsize)
            else:
                print 'Corrupt ACK' + str(Num)
                    
    except socket.error, msg:
        print 'Error code: ' + str(msg[0]) + 'Message ' + msg[1]
        sys.exit()
    

