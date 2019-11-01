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
  print("Failed to create socket. Error code: " + str(msg[0]) + " , Error message : " + msg[1])
  sys.exit()

print ("Socket Created")

#defining host and ip
host = "localhost"
port = 5050

waitCall0 = True
waitAck0 = False
waitCall1 = False
waitAck1 = False

def make_pkt(id,checksum,msg):   
  sndpkt = bytearray(id)
  sndpkt.append(checksum)
  sndpkt.append(msg)
  return sndpkt  

while(1) :
    if waitCall0:
      msg = input("Enter message to send : ")
    
      sndpkt = make_pkt(b"0",ip_checksum(msg), str.encode(msg))
    
      t = Timer(1, s.sendto(sndpkt, (host,port)))
      t.start()
    try:
      d = s.recvfrom(1024)
      if d[0] != 0:
        
    except timeout:
