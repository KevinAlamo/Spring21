import sys

def readData(fname, perm):
    dataFile = open(fname, perm)
    data = []
    while(True):
        d = dataFile.read(2)
        if d == b'':
            break
        data.append(d)
    dataFile.close()
    return data


def processIP(ip_addr):
    res = []
    dot = ip_addr.find(".")
    res.append(ip_addr[0:dot])

    dot2 = ip_addr.find(".", dot + 1)
    res.append(ip_addr[dot+1:dot2])

    dot = ip_addr.find(".", dot2 + 1)
    res.append(ip_addr[dot2+1:dot])

    res.append(ip_addr[dot+1:])

    return res


def calcUdpLen():
    return len(info)*2 + 8  # length of data in bytes and the rest of the header


def checksum():
    pass


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

    info = readData(filename, 'rb')
    udpL = calcUdpLen()  # number of bytes
    udpL = format(udpL, "016b")  # changing to 16 bit representation

    checksum()



