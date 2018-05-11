import socket 
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' ,ERROR message:' +msg[1]
	sys.exit()

print 'Socket Created'

host = 'localhost'
port = 4703

try:
	remote_ip = socket.gethostbyname( host )

except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip

s.connect((remote_ip, port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

reply = s.recv(1024)

print reply

#send data

message = raw_input('Enter a message ')

try:
	s.sendall(message)

except socket.error:
	print 'Send Failed'
	sys.exit()

print 'Message sent successfully'


#revieve message
#reply = s.recv(1024)

#print ' INclient reply: ' + reply
