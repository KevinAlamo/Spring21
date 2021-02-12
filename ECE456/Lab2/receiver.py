import math
import sys
from ECE456.Lab1 import decrypt

def processIP(ip_addr):
    res = []
    dot = ip_addr.find(".")
    res.append(ip_addr[0:dot])

    dot2 = ip_addr.find(".", dot + 1)
    res.append(ip_addr[dot+1:dot2])

    dot = ip_addr.find(".", dot2 + 1)
    res.append(ip_addr[dot2+1:dot])

    res.append(ip_addr[dot+1:])

    rtn = ''
    for i in range(0, 4):
        res[i] = format(int(res[i]), "08b")
        rtn = rtn + res[i]
    return rtn


def calcUdpLen():
    return (len(data) - 4) * 2 + 8  # length of data in bytes and the rest of the header


def checksum():  # = psuedoh + sport + des_port + udpL + data + checksum(done at end)
    # psuedoh = sIP + dIP + zeros + protocol + udpL
    res = int(sIP, 2) + int(dIP, 2) + int.from_bytes(b'0', "big") + int.from_bytes(b'17', "big") + totL
    for d in data:
        res = res + int.from_bytes(d, "big")

    mask = 0b1111111111111111
    low16 = res & mask
    remainder = res >> 16
    while remainder > 0:
        res = low16 + remainder
        low16 = res & mask
        remainder = res >> 16

    # # adding checksum and repeating the process
    # res = res + res
    # low16 = res & mask
    # remainder = res >> 16
    # while remainder > 0:
    #     res = low16 + remainder
    #     low16 = res & mask
    #     remainder = res >> 16

    # calculating number of bits
    # in the number
    x = int(math.log2(res)) + 1

    # Inverting the bits one by one
    for i in range(x):
        res = (res ^ (1 << i))

    if res == 0:
        so_port = str(int.from_bytes(data[0], "big"))
        de_port = str(int.from_bytes(data[1], "big"))
        print("Datagram from source-address " + sys.argv[1] + " source-port " + so_port + " to dest-address " +
              sys.argv[2] + " dest-port " + de_port + "; Length " + str(totL) + " bytes.")
    else:
        raise ValueError('Checksum Error')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise ValueError('Incorrect num of args')
    # grabbing args
    sIP = sys.argv[1]
    dIP = sys.argv[2]
    # processing IP addresses
    sIP = processIP(sIP)
    dIP = processIP(dIP)
    # grabbing data
    datagramFile = sys.argv[3]
    data = decrypt.readData(datagramFile, 'rb')  # read in file contents
    # getting udp header
    # so_port = data[0]
    # de_port = data[1]
    # udpL = data[2]
    # check = data[3]
    totL = calcUdpLen()
    checksum()
    keys = decrypt.readKeys('decryptKeys.txt', 'rb')
    f = decrypt.decrypt(data[4:], keys)
    decrypt.outfile(f)

