import socket
import sys
from ECE456.Lab2 import sender

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) != 4:
        raise ValueError('Incorrect num of args')
    sender.sIP = socket.gethostname()
    if isinstance(sender.sIP, str):
        print("worked")
    sender.dIP = sender.processIP(sys.argv[1])
    sender.de_port = int(sys.argv[2])
    sender.so_port = sender.de_port
    s.bind((sender.sIP, sender.de_port)) # TODO change to dIP when done

    filename = sys.argv[3]
    datagram_output = "msg"

    sender.info = sender.encrypt.readData(filename, 'rb')
    sender.udpL = sender.calcUdpLen()  # number of bytes
    print("LENGTH: " + str(sender.udpL))

    # psuedoh = sIP + dIP + zeros + protocol + udpL

    # encrypt.encrypt(info, )
    # print(int(protocol, 2))

    keys = sender.encrypt.readKeys("keyall1", 'rb')
    info = sender.encrypt.encrypt(sender.info, keys)
    sender.addpadding(info)
    check = sender.checksum()
    print("THE CHECK: " + str(check))
    datag = sender.setDatagram()

    file = open(datagram_output, 'wb')  # writing to the file
    for c in datag:
        file.write(c)
    file.close()

