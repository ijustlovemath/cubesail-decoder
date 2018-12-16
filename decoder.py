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
    
    print("Thank you SO MUCH for decoding a beacon for us, it means the world! Here's what you need to know:\n\n")
    print("==> Communications settings:")
    print("\tFrequency: 437.305MHz")
    print("\tModulation: GMSK")
    print("\tBandwidth: 75kHz")
    print("\tLink Layer: AX.25/HDLC")
    print("\tCallsign (CubeSail A): xxxxxx")
    print("\tCallsign (CubeSail B): yyyyyy")
    print("\tTLE:\n")
    print("cubesail_temp")
    print("1 99999U          18350.31100694  .00048519  00000-0  21968-2 0 00004")
    print("2 99999 085.0351 178.2861 0013006 291.7248 120.7146 15.20874873000012")

    print("\n")

    callsign = input('What is the callsign you received? (default: CQ) ')
    if callsign == "":
        callsign = "CQ    "

    print("\n\tNOTE: Payloads will come over RF in raw binary, but you may "
        +"enter it just using the hexadecimal strings you're familiar with\n")
    payload = input('What is the payload you received, in hexadecimal encoded ASCII? ')

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

def scan_u64(buf, offset, endian=ENDIANNESS):
    return scan_core(buf, offset, endian + "Q")

def scan_print3(description, value):
    print('{:40s}\t:\t{}'.format(description, value))

def main():
    callsign, payload = get_payload3()
    scan_print3("Payload", payload)
    for endian, description in zip(
        ["<", ">"], ['Little endian', 'Big endian']):
        offset = 0
        print('\n\n<<===[[[ {} beacon data decoding ]]]===>>'.format(description))
        # Powerboard beacon data
        print('\n==> Powerboard data')
        for name in ['Pack A Total Voltage'
            , 'Pack A Lower-Cell Voltage'
            , 'Pack B Total Voltage'
            , 'Pack B Lower-Cell Voltage'
            , 'Pack A Upper-Cell Temperature'
            , 'Pack A Lower-Cell Temperature'
            , 'Pack B Upper-Cell Temperature'
            , 'Pack B Lower-Cell Temperature']:
            value, offset = scan_double(payload, offset, endian=endian)
            scan_print3('\t'+name, value)
        # ADCS Beacon Data
        print('\n==> ADCS data')
        for name in ['q[0]'
            , 'q[1]'
            , 'q[2]'
            , 'q[3]'
            , 'w[0]'
            , 'w[1]'
            , 'w[2]']:
            value, offset = scan_double(payload, offset, endian=endian)
            scan_print3('\t'+name, value)
        value, offset = scan_u16(payload, offset, endian=endian)
        scan_print3('\tIllumination state', value)

        value, offset = scan_u8(payload, offset, endian=endian)
        scan_print3('\tAlgorithm', value)
        # Lithium Beacon Data
        print('\n==> Lithium radio data (ignore)')
        value, offset = scan_float(payload, offset, endian=endian)
        scan_print3('\tRadio Temperature', value)

        # HMD Beacon Data
        print('\n==> Health monitor data')
        value, offset = scan_u16(payload, offset, endian=endian)
        scan_print3('\tSync bytes', value)

        value, offset = scan_u8(payload, offset, endian=endian)
        scan_print3('\tHost ID', value)

        value, offset = scan_u32(payload, offset, endian=endian)
        scan_print3('\tSystem time', value)

        value, offset = scan_u64(payload, offset, endian=endian)
        scan_print3('\tRecovery mode', value)

        value, offset = scan_float(payload, offset, endian=endian)
        scan_print3('\tC&DH Temperature', value)

    print('\n\nThank you for your help! Please email this printout to dejourn2@illinois.edu, with subject \"BEACON DATA\"')

if __name__ == '__main__':
    main()
