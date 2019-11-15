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

def make_pkt(id,msg,checksum):   
  sndpkt = str(id) + msg + checksum
  return sndpkt

def send_pkt(sndpkt, id):
  s.sendto(sndpkt, (host,port))
  d = s.recvfrom(1024)
  data = d[0]
  
def listen_ack(id):
  while data[0] != id: # or sndpkt[-2:] != data[1:]:
    d = s.recvfrom(1024)
    data = d[0]

#variables set here
timeout = 2 # 2 seconds
packets = range(10) #size of sequence is 10; it will wrap around
N = 4 #size of window is 4
base = 0
nextseqnum = 0
data = ["h", "e", "l", "l", "o", "w", "o", "r", "l", "d"]

while(1):
    if (nextseqnum < base + N):
      if(base == nextseqnum):
        packets[base]   = make_pkt(base, data[base], ip_checksum(data[base]))
        packets[base+1] = make_pkt(base+1, data[base+1], ip_checksum(data[base+1]))
        packets[base+2] = make_pkt(base+2, data[base+2], ip_checksum(data[base+2]))
        packets[base+3] = make_pkt(base+3, data[base+3], ip_checksum(data[base+3]))
        send_pkt(packets[base], base)
        send_pkt(packets[base+1], base+1)
        send_pkt(packets[base+2], base+2)
        send_pkt(packets[base+3], base+3)
        t = threading.Thread(target=listen_ack, args=(base))
        t.start()
        t.join(timeout)
        while t.isAlive(): #timed out
        #send all packets in the window
          send_pkt(packets[base], base)
          send_pkt(packets[base+1], base+1)
          send_pkt(packets[base+2], base+2)
          send_pkt(packets[base+3], base+3)
          t = threading.Thread(target=listen_ack, args=(base))
          t.start()
          t.join(timeout)

        nextseqnum += 4
        base += 1

      else:
        packets[nextseqnum] = make_pkt(nextseqnum, data[nextseqnum], ip_checksum(data[nextseqnum]))
        send_pkt(packets[nextseqnum], nextseqnum)
        t = threading.Thread(target=listen_ack, args=(base))
        t.start()
        t.join(timeout)
        while t.isAlive(): #timed out
          send_pkt(packets[base], base)
          send_pkt(packets[base+1], base+1)
          send_pkt(packets[base+2], base+2)
          send_pkt(packets[base+3], base+3)
          t = threading.Thread(target=listen_ack, args=(base))
          t.start()
          t.join(timeout)
        nextseqnum += 1
        base += 1

s.close()