import sys


def processIP(ip_addr):
    res = []
    res.append(ip_addr[0:ip_addr.find(".")])
    res.append(ip_addr[len(res[1]):])


if __name__ == '__main__':
    if len(sys.argv) != 7:
        raise ValueError('No key or data file')
    filename = sys.argv[1]
    sourceIP = sys.argv[2]
    destIP = sys.argv[3]
    so_port = sys.argv[4]
    de_port = sys.argv[5]
    datagram_output = sys.argv[6]
    processIP(sourceIP)
