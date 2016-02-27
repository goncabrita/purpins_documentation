import socket
import sys
import crcmod.predefined
import struct

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    header = [0x40, 0x01, 0x00]

    msg = "".join(map(chr, header))

    crc = crcmod.predefined.Crc('crc-8')
    crc.update(msg)

    msg += chr(crc.crcValue)

    print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)
    
    conn.sendall(msg)
    
    reply = conn.recv(1024)
    
    print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

    reply_components = struct.unpack('5B', reply)

    crc = crcmod.predefined.Crc('crc-8')
    crc.update(reply[0:4])

    if crc.crcValue != reply_components[4]:
        print "ERROR! CRC does not match!"
        sys.exit(2)

    print "Version " + str(reply_components[3])

conn.close()
s.close()