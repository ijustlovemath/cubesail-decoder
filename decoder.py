'''
    CubeSail Beacon Decoder
    Written with love by Jeremy DeJournett
    2018/12/16
'''

from __future__ import print_function # nop in py3, adding py2 support
import struct
from struct import calcsize
import binascii
import sys
from collections import OrderedDict


# Little endian CPU
ENDIANNESS = "<"

def python3():
    return sys.version_info[0] == 3

def get_string(description):
    if python3():
        return input(description)
    else:
        return raw_input(description)
    
def get_payload3():
    
    print("Thank you SO MUCH for decoding a beacon for us, it means the world! Here's what you need to know:\n\n")
    print("==> Communications settings:")
    print("\tFrequency: 437.305MHz")
    print("\tModulation: GMSK (GR3UH scrambling)")
    print("\tBandwidth: 15kHz")
    print("\tBaud rate: 9600")
    print("\tLink Layer: AX.25/HDLC")
    print("\tCallsign: WI2XVF")
    print("\tTLE:\n")
    print("cubesail_temp")
    print("1 99999U          18350.31100694  .00048519  00000-0  21968-2 0 00004")
    print("2 99999 085.0351 178.2861 0013006 291.7248 120.7146 15.20874873000012")

    print("\n")

    callsign = get_string('What is the callsign you received? (default: CQ) ')
    if callsign == "":
        callsign = "CQ    "

    print("\n\tNOTE: Payloads will come over RF in raw binary, but you may "
        +"enter it just using the hexadecimal strings you're familiar with\n")
    payload = get_string('What is the payload you received, in hexadecimal encoded ASCII? ')

    return callsign, binascii.unhexlify(payload)

def scan_core(buf, offset, fmt):
    try:
        return struct.unpack_from(fmt, buf, offset)[0], offset+calcsize(fmt)
    except struct.error:
        print("\n\n[ERROR] The payload you provided is not long enough!\n\n")
        raise

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

def scan_u64(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "Q")

def scan_print3(description, value):
    print('{:40s}\t:\t{}'.format(description, value))

def payload_dict(payload, endian=ENDIANNESS):
    payload_d = OrderedDict()
    offset = 0
    section = 'Powerboard data'
    for name in ['Pack A Total Voltage'
        , 'Pack A Lower-Cell Voltage'
        , 'Pack B Total Voltage'
        , 'Pack B Lower-Cell Voltage'
        , 'Pack A Upper-Cell Temperature'
        , 'Pack A Lower-Cell Temperature'
        , 'Pack B Upper-Cell Temperature'
        , 'Pack B Lower-Cell Temperature']:
        value, offset = scan_double(payload, offset, endian=endian)
        payload_d[section, name] = value

    section = 'ADCS data'
    for name in ['q[0]'
        , 'q[1]'
        , 'q[2]'
        , 'q[3]'
        , 'w[0]'
        , 'w[1]'
        , 'w[2]']:
        value, offset = scan_double(payload, offset, endian=endian)
        payload_d[section, name] = value
    value, offset = scan_u16(payload, offset, endian=endian)
    payload_d[section, 'Illumination state'] = value

    value, offset = scan_u8(payload, offset, endian=endian)
    payload_d[section, 'Algorithm'] = value

    section = 'Lithium Radio data (ignore)'
    value, offset = scan_float(payload, offset, endian=endian)
    payload_d[section, 'Radio Temperature'] = value

    section = 'Health monitor data'
    # HMD Beacon Data
    value, offset = scan_u16(payload, offset, endian=endian)
    payload_d[section, 'Sync bytes'] = value

    value, offset = scan_u8(payload, offset, endian=endian)
    payload_d[section, 'Host ID'] = value

    value, offset = scan_u32(payload, offset, endian=endian)
    payload_d[section, 'System time'] = value

    value, offset = scan_u64(payload, offset, endian=endian)
    payload_d[section, 'Recovery mode'] = value

    value, offset = scan_float(payload, offset, endian=endian)
    payload_d[section, 'C&DH Temperature'] = value

    return payload_d

def print_payload_dict(payload_d):

    prev_section = None
    section_prefix = "\n==> "

    for key, value in payload_d.items():
        section, name = key
        if prev_section is None:
            print(section_prefix + section)
        else:
            if prev_section != section:
                print(section_prefix + section)

        scan_print3('\t'+name, value)
        prev_section = section

def interactive_decode():
    callsign, payload = get_payload3()
    scan_print3("Callsign", callsign)
    scan_print3("Payload", payload)

    for endian, description in zip(
        ["<", ">"], ['Little endian', 'Big endian']):
        print('\n\n<<===[[[ {} beacon data decoding ]]]===>>'.format(description))
        payload_d = payload_dict(payload, endian=endian)
        print_payload_dict(payload_d)

    print('\n\nThank you for your help! Please email this printout to dejourn2@illinois.edu, with subject \"BEACON DATA\"')

def main():
    interactive_decode()

if __name__ == '__main__':
    main()
