'''
    CubeSail Beacon Decoder
    Written with love by Jeremy DeJournett
    2018/12/16
'''

#from __future__ import print_function
import struct
from struct import calcsize
import binascii


# Little endian CPU
ENDIANNESS = "<"

def get_payload3():
    return "CQ    ", binascii.unhexlify("648382839293748382949473893949598395835938593483958304")

    callsign = input('What is the callsign you received? (default: CQ)')
    if callsign == "":
        callsign = "CQ    "

    payload = input('What is the payload you received, in hexadecimal encoded ASCII?')

    return callsign, binascii.unhexlify(payload)

def scan_core(buf, offset, fmt):
    return struct.unpack_from(fmt, buf, offset)[0], offset+calcsize(fmt)

def scan_double(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "d")

def scan_u8(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "B")

def scan_u16(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "H")

def scan_float(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "f")

def scan_u32(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "L")

def scan_print3(description, value):
    print('{}\t:\t{}'.format(description, value))

def main():
    callsign, payload = get_payload3()
    scan_print3("Payload", payload)
    for endian, description in zip(
        ["<", ">"], ['Little endian', 'Big endian']):
        offset = 0
        print('{} beacon data decoding:'.format(description))
        # Powerboard beacon data
        print('==> Powerboard data')
        for name in ['Pack A Total Voltage'
            , 'Pack A Lower-Cell Voltage'
            , 'Pack B Total Voltage'
            , 'Pack B Lower-Cell Voltage'
            , 'Pack A Upper-Cell Temperature'
            , 'Pack A Lower-Cell Temperature'
            , 'Pack B Upper-Cell Temperature'
            , 'Pack B Lower-Cell Temperature']:
            value, offset = scan_double(payload, offset, endian=endian)
            scan_print3(name, value)
        # ADCS Beacon Data
        print('==> ADCS data')
        for name in ['q[0]'
            , 'q[1]'
            , 'q[2]'
            , 'q[3]'
            , 'w[0]'
            , 'w[1]'
            , 'w[2]']:
            value, offset = scan_double(payload, offset, endian=endian)
            scan_print3(name, value)
        value, offset = scan_u16(payload, offset, endian=endian)
        scan_print3('Illumination state', value)

        value, offset = scan_u8(payload, offset, endian=endian)
        scan_print3('Algorithm', value)
        # Lithium Beacon Data
        print('==> Lithium radio data (ignore)')
        value, offset = scan_float(payload, offset, endian=endian)
        scan_print3('Radio Temperature', value)

        # HMD Beacon Data
        print('==> Health monitor data')
        value, offset = scan_u16(payload, offset, endian=endian)
        scan_print3('Sync bytes', value)

        value, offset = scan_u8(payload, offset, endian=endian)
        scan_print3('Host ID', value)

        value, offset = scan_u32(payload, offset, endian=endian)
        scan_print3('System time', value)

        value, offset = scan_u64(payload, offset, endian=endian)
        scan_print3('Recovery mode', value)

        value, offset = scan_float(payload, offset, endian=endian)
        scan_print3('C&DH Temperature', value)

    print('Thank you for your help! Please email this printout to dejourn2@illinois.edu, with subject \"BEACON DATA\"')

if __name__ == '__main__':
    main()
