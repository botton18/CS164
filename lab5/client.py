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

count = 0

seq = '0'
packet = ''
prevous = 0
while(count < 10):
    #msg = raw_input('Enter message to send: ')
    print 'Client_SEQNUMBER: ' + seq
    msg = str(count)
    
    #if count == 2:
    #    checksum = ip_checksum(msg) + '123'
    #else:
    #    checksum = ip_checksum(msg)
    checksum = ip_checksum(msg)
    packet = seq + str(msg) + str(checksum)
    try:
        #set string
        s.sendto(packet,(host,port))
        #start timer
        checksum = ip_checksum(msg)
        packet = seq + str(msg) + str(checksum)
        t = threading.Timer(2,s.sendto, [packet,(host,port)])
        t.start()
        #receive dat from client

        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        #print 'Server reply : ' + reply
        
        ACK = reply[0]
        ACKchecksum = reply[1:]
        print 'ACK From Server: ' + ACK
        ACK_to_check = ip_checksum(ACK)

        if ACK == seq and ACK_to_check == ACKchecksum:
            print 'ACK SUCCESS'
            t.cancel()
        else:
            print 'Resending packet'
        while(ACK != seq or ACK_to_check != ACKchecksum):
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
            ACK = reply[0]
            ACKchecksum = reply[1:]
            ACK_to_check = ip_checksum(ACK)

    except socket.error,msg:
        print 'Error sending msg'
        sys.exit()
    
    previous = count
    count = count + 1
    
    if seq == '0':
        seq = '1'
    else:
        seq = '0'
    print '----------------------------------------------------'
#Enter Message to send: hello
#Server reply : OK....hello

