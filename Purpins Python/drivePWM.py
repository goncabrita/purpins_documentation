import serial
import crcmod.predefined
import struct
import sys

if len(sys.argv) != 3:
    print "usage: drivePWM.py <left_pwm> <right_pwm>"
    sys.exit(2)

if int(sys.argv[1]) < -255 or int(sys.argv[1]) > 255 or int(sys.argv[2]) < -255 or int(sys.argv[2]) > 255:
    print "usage: *_pwm between -255 and 255"
    sys.exit(2)

port = serial.Serial(port='/dev/tty.usbmodem0E20D771', baudrate=115200)

header = [0x40, 0x04, 0x08]

msg = "".join(map(chr, header))
msg += struct.pack("2i", int(sys.argv[1]), int(sys.argv[2]))

crc = crcmod.predefined.Crc('crc-8')
crc.update(msg)

msg += chr(crc.crcValue)

print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)

port.write(msg)

reply = port.read(4)

print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

port.close()