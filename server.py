import socket
import sys
from check import ip_checksum

Host = "" #all available interfaces
Port = 5000 #random number based on my sid

#creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print "socket created"

#binding socket
try:
  s.bind((Host, Port)) #tuple again
except socket.error as msg:
  print "Bind failed. Error code: " + str(msg[0]) + " Message: " +str(msg[1])
  sys.exit()

print "socket bind complete"

wait0 = True

while 1:
  if wait0:
    while 1:
      d = s.recvfrom(1024)
      data = d[0]
      addr = d[1]
      
      # if ip_checksum(data[1:]):
      #   reply = "1" + ip_checksum(data[1:])
      #   s.sendto(reply, addr)

      if data[0] == "1": #should be elif
        reply = "1" + ip_checksum(data[1:])
        s.sendto(reply, addr)

      else:
        break

    print "Message[" + addr[0] + ":" + str(addr[1]) + "] - " + data[1:-2]
    reply = "0" + ip_checksum(data[1:])
    s.sendto(reply, addr)
    wait0 = False
  
  else:
    while 1:
      d = s.recvfrom(1024)
      data = d[0]
      addr = d[1]
      
      # if corrupt:
      #  reply = "1" + ip_checksum(data[1:])
      #  s.sendto(reply, addr)

      if data[0] == "0": #should be elif
        reply = "0" + ip_checksum(data[1:])
        s.sendto(reply, addr)

      else:
        break
    #print data
    print "Message[" + addr[0] + ":" + str(addr[1]) + "] - " + data[1:-2]
    reply = "1" + ip_checksum(data[1:])
    s.sendto(reply, addr)
    wait0 = True


s.close()
