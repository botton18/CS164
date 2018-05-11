import socket
import sys
from thread import *
HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try: 
	s.bind((HOST,PORT))
except socket.error ,msg:
	print 'Bind failed ' + str(msg[0]) + ' ' + msg[1]
	sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

def clientthread(conn,s,thelist):
	conn.send('Welcome to the server\n')
	while True:
		data = conn.recv(1024)
		#reply = 'ServerReplay ' + data
		if not data:
			break
		#conn.sendall(reply)
		#print 'data is from client: ' + data[0:2]
		conn.send('From SERVER: You said ' + data)	
		if data[0:2] == "!q":
			print 'Closing connection'
			#conn.close()
			thelist.remove(conn)
			break
		if data[0:2] == "!l":
			print len(thelist)
		
		if data[0:8] == "!sendall":
			print 'IN SENDALL'
			reply = data[8:len(data)]
			for i in thelist:
				i.send(reply)
			#conn.send("HELLO")
	conn.close()
	s.close()

#wait to accept a connection 
mylist = []
while 1:
	
	conn, addr = s.accept()
	mylist.append(conn)
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
#keep talking to client

	start_new_thread(clientthread ,(conn,s,mylist))
	print 'out of start_newthread\n'
	print len(mylist)
	
	#data = conn.recv(1024)
	#reply = 'Ok....' + data
	#if not data:
	#	break

	#conn.sendall(reply)
	
	#print len(mylist)
	#if data == "!q":
	#	print 'Closing connection'
	#	break

	#if data == "!l":
	#	print len(mylist)

	#print ' DATA FROM CLIENT ' + data 

#conn.close()
#s.close()
