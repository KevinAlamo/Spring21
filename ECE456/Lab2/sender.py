import math
import sys
from ECE456.Lab1 import encrypt


# processes given ip
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


# calculates the total length
def calcUdpLen():
    res = 0
    for x in info:
        res = res + len(x)
    return res + 8  # length of data in bytes and the rest of the header


# calculate the checksum
def checksum():
    res = int(sIP[:16], 2) + int(sIP[16:], 2) + int(dIP[:16], 2) + int(dIP[16:], 2) + 0 + 17 + udpL
    res = res + so_port + de_port + udpL
    for d in info:
        if len(d) == 1:
            d = d + b'\x00'
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


# sets up the datagram that will be sent
def setDatagram():
    datagram = []
    datagram.append(so_port.to_bytes(2, 'big'))
    datagram.append(de_port.to_bytes(2, 'big'))
    datagram.append(udpL.to_bytes(2, 'big'))
    datagram.append(check.to_bytes(2, 'big'))

    for x in info:
        datagram.append(x)
    return datagram


def addpadding(info):
    dataLen = 0
    for i in info:
        dataLen = dataLen + len(i)

    if dataLen%2 == 1:
        info[len(info)-1] = info[len(info)-1] + b'\x00'




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
    print("LENGTH: " + str(udpL))

    # psuedoh = sIP + dIP + zeros + protocol + udpL

    # encrypt.encrypt(info, )
    # print(int(protocol, 2))


    keys = encrypt.readKeys("../Lab4/keyall1", 'rb')
    info = encrypt.encrypt(info, keys)
    addpadding(info)
    check = checksum()
    print("THE CHECK: " + str(check))
    datag = setDatagram()

    file = open(datagram_output, 'wb')  # writing to the file
    for c in datag:
        file.write(c)
    file.close()
