import math
import sys
from ECE456.Lab1 import decrypt


# separates the ip given
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



# calculates the checksum
def checksum():  # = psuedoh + sport + des_port + udpL + data
    # psuedoh = sIP + dIP + zeros + protocol + udpL
    res = int(sIP, 2) + int(dIP, 2) + 0 + 17 + int.from_bytes(udpL,"big")
    for i in range(0, 4):
        res = res + int.from_bytes(data[i], "big")

    for d in f:
        if len(d) == 1:
            d = d + b'\x00'
        res = res + int.from_bytes(d, "big")

    mask = 0b1111111111111111 # mask used to grab ls 16bits
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
              sys.argv[2] + " dest-port " + de_port + "; Length " + str(udpL) + " bytes.")
    else:
        raise ValueError('Checksum Error')


def removepadding(f):
    dataLen = 0
    for i in f:
        dataLen = dataLen + len(i)

    if dataLen * 2 > int.from_bytes(udpL, "big") - 8:
        f[len(f) - 1] = f[len(f) - 1][:1]


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
    keys = decrypt.readKeys('keyall1', 'rb')
    f = decrypt.decrypt(data[4:], keys)
    # getting udp header
    # so_port = data[0]
    # de_port = data[1]
    udpL = data[2]
    # check = data[3]
    checksum()
    removepadding(f)

    decrypt.outfile(f)

