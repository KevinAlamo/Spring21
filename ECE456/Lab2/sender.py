import math
import sys
from ECE456.Lab1 import encrypt


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
    for i in range(0,4):
        res[i] = format(int(res[i]), "08b")
        rtn = rtn + res[i]
    return rtn


def calcUdpLen():
    return len(info) * 2 + 8  # length of data in bytes and the rest of the header

# calculate the checksum
def checksum():
    res = int(sIP, 2) + int(dIP, 2) + int.from_bytes(zeros, "big") + int.from_bytes(protocol, "big") + udpL
    res = res + so_port + de_port + udpL
    for d in info:
        res = res + int.from_bytes(d, "big")

    mask = 0b1111111111111111
    low16 = res & mask
    remainder = res >> 16
    while remainder > 0:
        res = low16 + remainder
        low16 = res & mask
        remainder = res >> 16

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

    return res


def setDatagram():
    datagram = []
    datagram.append(so_port.to_bytes(2, 'big'))
    datagram.append(de_port.to_bytes(2, 'big'))
    datagram.append(udpL.to_bytes(2, 'big'))
    datagram.append(check.to_bytes(2, 'big'))
    for x in info:
        datagram.append(x)
    return datagram



if __name__ == '__main__':
    if len(sys.argv) != 7:
        raise ValueError('Incorrect num of args')
    # grabbing the arguments
    filename = sys.argv[1]
    sourceIP = sys.argv[2]
    destIP = sys.argv[3]
    so_port = sys.argv[4]
    de_port = sys.argv[5]
    datagram_output = sys.argv[6]
    # processing the inputs
    sIP = processIP(sourceIP)
    dIP = processIP(destIP)

    so_port = int(so_port)
    de_port = int(de_port)

    info = encrypt.readData(filename, 'rb')
    udpL = calcUdpLen()  # number of bytes

    zeros = b'0'
    protocol = b'17'
    # psuedoh = sIP + dIP + zeros + protocol + udpL

    # encrypt.encrypt(info, )
    # print(int(protocol, 2))

    check = checksum()
    datag = setDatagram()

    file = open(datagram_output, 'wb')
    for c in datag:
        file.write(c)
    file.close()
