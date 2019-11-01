import socket
import sys

from _thread import *
'''
def clientthread(conn,client_list):
  #sending message to connected client
  conn.send(b"Welcome to the server. Type something and hit enter\n")
  
  while True:
  
    data = conn.recv(1024)
    reply = b"Ok..." + data
    if not data or data[0:2] == b"!q" :
      break
    if data[0:9] == b"!sendall ":
      for member in client_list:
        member.sendall(reply[9:])
    else:
      conn.sendall(reply)

  conn.close()

'''
Host = "" #all available interfaces
Port = 5050 #random number based on my sid

#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ("socket created")

#binding socket
try:
  s.bind((Host, Port)) #tuple again
except socket.error as msg:
  print ("Bind failed. Error code: " + str(msg[0]) + "Message: " +str(msg[1]))
  sys.exit()

print("socket bind complete")

#listening
#s.listen(10) #10 is the backlog; number of incoming connections that can wait; 11th will be rejected
#print("socket now listening")

#client_list =[]
#send message back to client
while 1:
  #conn, addr = s.accept() #conn is the socket object and addr is ip:port
  #print("Connected with " + addr[0] + ":" + str(addr[1]))
  
  #client_list.append(conn)
  
  #start_new_thread(clientthread, (conn,client_list))
  
  d =  s.recvfrom(1024)
  data = d[0]
  addr = d[1]

  if not data:
    break

  reply = b"OK... " + data 

  s.sendto(reply, addr)
  print("Message[" + addr[0] + ":" + str(addr[1]) + "] - " + data.decode().strip())

s.close()
