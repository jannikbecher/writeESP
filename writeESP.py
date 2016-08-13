#!/usr/bin/env python

import time
import serial
import sys
import ntpath
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="The file which should be uploaded")
parser.add_argument("-p", "--port", help="Path to serial device", default="/dev/ttyUSB0")
parser.add_argument("-b", "--baudrate", type=int, help="Set the baudrate (9600/57600/115200/...)", default=9600)
parser.add_argument("--delay", type=float, help="Set the delay time after each command (in s)", default=0.2)
parser.add_argument("--parity", choices=['O', 'E'], help="Set parity to ODD (O) or EVEN (E)", default=serial.PARITY_ODD)
parser.add_argument("--stopbits", type=int, help="Set number of stopbits", default=serial.STOPBITS_TWO)
parser.add_argument("--bytesize", type=int, help="Set the bytesize", default=serial.SEVENBITS)
args = parser.parse_args()

# configure the serial connections
uart = serial.Serial(
        port=args.port,
        baudrate=args.baudrate,
        parity=args.parity,
        stopbits=args.stopbits,
        bytesize=args.bytesize
)

uart.isOpen()

filename = ntpath.basename(args.filename)
delay = args.delay

with open(args.filename, "r") as file:
    uart.write(("file.remove(\"" + filename + "\")\r\n").encode())
    time.sleep(delay)
    uart.write(("file.open(\"" + filename + "\", \"w\")\r\n").encode())
    time.sleep(delay)
    uart.write(("w = file.writeline \r\n").encode())
    time.sleep(delay)
    for line in file.read().splitlines():
        uart.write(("w([[" + line + "]])\r\n").encode())
        time.sleep(delay)
    uart.write(("file.close()\r\n").encode())
    time.sleep(delay)
    uart.write(("dofile(\"" + filename + "\")\r\n").encode())
    time.sleep(delay)
