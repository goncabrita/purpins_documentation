import serial
import crcmod.predefined
import struct
import sys

if len(sys.argv) < 3:
    print "usage: getSensorsPack.py <sensor_1> <sensor_2> ... <sensor_n>"
    sys.exit(2)

port = serial.Serial(port='/dev/tty.usbmodem0E20D771', baudrate=115200)

header = [0x40, 0x15, 0x00]

msg = "".join(map(chr, header))

crc = crcmod.predefined.Crc('crc-8')
crc.update(msg)

msg += chr(crc.crcValue)

print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)

port.write(msg)

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