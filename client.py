#client.py // rdt 3.0 sender
import socket
import sys
from check import ip_checksum
import threading
import time

try:
  #Address Family IPv4, SOCK_STREAM is TCP, SOCK_DGRAM is UDP
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
  print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
  sys.exit() 

print "Socket Created"

#defining host and ip
host = "localhost"
port = 5000
timeout = 2

waitCall0 = True

def make_pkt(id,checksum,msg):   
  sndpkt = id + msg + checksum
  return sndpkt

def send_pkt(sndpkt, id):
  s.sendto(sndpkt, (host,port))
  d = s.recvfrom(1024)
  data = d[0]
  #print data
  while data[0] != id: # or sndpkt[-2:] != data[1:]:
    d = s.recvfrom(1024)
    data = d[0]

while(1):
    if waitCall0:
      msg = raw_input("Enter message to send : ")
      sndpkt = make_pkt("0",ip_checksum(msg), msg)

      #do-while
      t = threading.Thread(target=send_pkt, args=(sndpkt,"0"))
      t.start()
      t.join(timeout)
      while t.isAlive():
        t = threading.Thread(target=send_pkt, args=(sndpkt,"0"))
        t.start()
        t.join(timeout)
      
      waitCall0 = False

    else:
      msg = raw_input("Enter message to send : ")
      sndpkt = make_pkt("1",ip_checksum(msg), msg)

      #do-while
      t = threading.Thread(target=send_pkt, args=(sndpkt,"1"))
      t.start()
      t.join(timeout)
      while t.isAlive():
        t = threading.Thread(target=send_pkt, args=(sndpkt,"1"))
        t.start()
        t.join(timeout)
      
      waitCall0 = True

s.close()