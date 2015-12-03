#!/usr/bin/env python
# udpDFbit0.py
from scapy.all import *
import sys
from random import randint
# Usage: ./udpDFbit0.py [payload length] [dest IP] [dest Port]
# UDP echo datagram that is below LAN/Downstream MTU 1500 and is max size for WAN/Upstream MTU 1500
# This datagram should not be fragmented by MAP-T CE
# Example:./udpDFbit0.py 1452 8.8.8.8 7
# UDP echo datagram that max for LAN/Downstream MTU 1500 but is above max size for WAN/Upstream MTU 1500
# This datagram should be fragmented by MAP-T CE
# Example:./udpDFbit0.py 1472 8.8.8.8 7
def testError(errstr):
    print("The Test has Failed")
    print("{}".format(errstr))
    sys.exit(1)
payload = ''

for x in range(int(sys.argv[1])):
    payload += str(randint(0,9))

i = IP()
i.flags = 0
i.ttl = 32
i.dst = sys.argv[2]
u = UDP()
u.dport = int(sys.argv[3])
u.sport = randint(50000,60000)

p = sr1(i/u/payload,timeout=1)

try:
    if ( p[IP].dst ):
        print("Received reply")
except:
    print("Test Failed: No reply received")
    sys.exit(1)

if ( p[IP].dst == i.src ):
    print("True: Reply to correct client IP")
else:
    testError("False: Client IP")

if ( p[IP].src == i.dst ):
    print("True: Reply from correct server IP")
    sys.exit(1)
else:
    testError("False: Server IP")

if ( p[UDP].sport == u.dport ):
    print("True: Reply from correct server port")
else:
    testError("False: Server port")

if ( p[UDP].dport == u.sport ):
    print("True: Reply to correct client port")
else:
    testError("False: Client Port")

if ( p[Raw].load == payload ):
    print("True: Payload values match")
else:
    testError("False: Payload")

print("Test Completed Successfully")
