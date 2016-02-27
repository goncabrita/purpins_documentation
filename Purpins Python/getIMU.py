import serial
import crcmod.predefined
import struct
import sys

port = serial.Serial(port='/dev/tty.usbmodem0E20D771', baudrate=115200)

header = [0x40, 0x08, 0x00]

msg = "".join(map(chr, header))

crc = crcmod.predefined.Crc('crc-8')
crc.update(msg)

msg += chr(crc.crcValue)

print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)

port.write(msg)

reply = port.read(44)

print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

reply_components = struct.unpack('!3B10fB', reply)

crc = crcmod.predefined.Crc('crc-8')
crc.update(reply[0:43])

print reply_components

if crc.crcValue != reply_components[13]:
    print "ERROR! CRC does not match!"
    sys.exit(2)

print " "
print "Quaternion"
print "x " + str(reply_components[3])
print "y " + str(reply_components[4])
print "z " + str(reply_components[5])
print "w " + str(reply_components[6])
print " "
print "Angular Velocity"
print "x " + str(reply_components[7])
print "y " + str(reply_components[8])
print "z " + str(reply_components[9])
print " "
print "Linear Velocity"
print "x " + str(reply_components[10])
print "y " + str(reply_components[11])
print "z " + str(reply_components[12])
print " "

port.close()