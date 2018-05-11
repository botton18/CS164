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

seq = '0'
count = 0
while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    print "Sever_SEQNUMBER: " + seq   
    if not data:
        break
    toconcat = data.strip()
    senderseq = toconcat[0]
    sendermsg = toconcat[1]
    senderchecksum = toconcat[2:len(toconcat)] 
    
    #reply = 'OK...' + data
    checksum = ip_checksum(sendermsg)
    if checksum == senderchecksum and int(seq) == int(senderseq):
        if seq == '0':
            seq = '1'
        else:
            seq = '0'
        Ackchecksum = ip_checksum(senderseq)
        print 'Seq to send to client:  ' + senderseq
        packet = senderseq + Ackchecksum
        if sendermsg == '2':
            print 'Timing OUT'
            t = threading.Timer(2.01 ,s.sendto, [packet,addr])
            t.start()
        else:
            s.sendto(packet, addr)
    elif checksum != senderchecksum:
        if checksum != senderchecksum:
            print 'Checksum not matching'
        if seq != senderseq:
            print 'Seq not matching'
        
        if int(senderseq) == 0:
            senderseq = '1'
        else:
            senderseq = '0'
        Ackchecksum = ip_checksum(senderseq)
        packet = senderseq + Ackchecksum
        print 'Seq to send to client: ' + senderseq
        s.sendto(packet, addr)
    else:
        Ackchecksum = ip_checksum(senderseq)
        packet = senderseq + Ackchecksum
        s.sendto(packet,addr)
        print 'Sending duplicate ACK'
    #s.sendto(packet,addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + sendermsg
    count = count + 1
    print '----------------------------------------------------'
s.close()
