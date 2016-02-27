import serial
import crcmod.predefined
import struct
import sys

if len(sys.argv) < 3:
    print "usage: setSensorsPack.py <sensor_1> <sensor_2> ... <sensor_n>"
    sys.exit(2)

header = [0x40, 0x14, len(sys.argv)-1]

for sensor in sys.argv[1:]:
    if int(sensor) < 5 or int(sensor) > 10:
        print "Sensor " + sensor + " does not exist."
        sys.exit(2)
    header.append(int(sensor))

port = serial.Serial(port='/dev/tty.usbmodem0E20D771', baudrate=115200)

msg = "".join(map(chr, header))

crc = crcmod.predefined.Crc('crc-8')
crc.update(msg)

msg += chr(crc.crcValue)

print "Request " + " ".join("{:#04X}".format(ord(i)) for i in msg)

port.write(msg)

reply = port.read(4)

print "Reply   " + " ".join("{:#04X}".format(ord(i)) for i in reply)

port.close()