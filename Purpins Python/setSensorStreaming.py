import serial
import crcmod.predefined
import struct
import sys

if len(sys.argv) != 2:
    print "usage: setStreamingFrequency.py <streaming_frequency>"
    sys.exit(2)

port = serial.Serial(port='/dev/tty.usbmodem0E20D771', baudrate=115200)

header = [0x40, 0x16, 0x04]

msg = "".join(map(chr, header))
msg += struct.pack("1f", float(sys.argv[1]))

crc = crcmod.predefined.Crc('crc-8')
crc.update(msg)

msg += chr(crc.crcValue)

print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)

port.write(msg)

reply = port.read(4)

print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

var = 1
while var == 1:
    reply = port.read(3)
    reply += port.read(ord(reply[2])+1)

    print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

#reply_components = struct.unpack('!3B2fB', reply)

#crc = crcmod.predefined.Crc('crc-8')
#crc.update(reply[0:len(reply)-1])

#if crc.crcValue != reply_components[5]:
#    print "ERROR! CRC does not match!"
#    sys.exit(2)

#print " "
#print "Left  " + str(reply_components[3])
#print "Right " + str(reply_components[4])
#print " "

port.close()