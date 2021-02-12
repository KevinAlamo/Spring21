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


def checksum():  # = psuedoh + sport + des_port + udpL + data + checksum(done at end)
    # psuedoh = sIP + dIP + zeros + protocol + udpL
    res =



if __name__ == '__main__':
    if len(sys.argv) != 7:
        raise ValueError('No key or data file')
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
    so_port = format(so_port, "016b")  # changing to 16 bit representation
    de_port = int(de_port)
    de_port = format(de_port, "016b")

    info = encrypt.readData(filename, 'rb')
    udpL = calcUdpLen()  # number of bytes
    udpL = format(udpL, "016b")  # changing to 16 bit representation

    zeros = format(0, "08b")
    protocol = format(17, "08b")
    # psuedoh = sIP + dIP + zeros + protocol + udpL

    # encrypt.encrypt(info, )
    # print(int(protocol, 2))

    checksum()



