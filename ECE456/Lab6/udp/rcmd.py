import socket
import sys
import sender
import encrypt


def sendMsg(msgs):
    res = b''
    for msg in msgs:
        res = b"".join([res, msg])

    return res

def prepdata(data):
    prev = 0
    res = []
    num = 0
    s = b''
    for i in data:
        temp = i.encode("ascii")
        s = b''.join([s, temp])
        if num == 1:
            res.append(s)
            num = 0
            s = b''
        else:
            num = num+1

    return res

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if len(sys.argv) != 6:
        raise ValueError('Incorrect num of args')
    sender.sIP = socket.gethostbyname(socket.gethostname())
    # if isinstance(sender.sIP, str):
    #     print("worked")
    sender.dIP = socket.gethostbyname(sys.argv[1])
    sender.de_port = int(sys.argv[2])
    sender.so_port = sender.de_port

    sender.sIP = sender.processIP(sender.sIP)
    tempIP = sender.dIP
    sender.dIP = sender.processIP(sender.dIP)

    sender.info = sys.argv[3] + "@" + sys.argv[4] + "@" + sys.argv[5] + "@"
    sender.info = prepdata(sender.info)
    sender.udpL = sender.calcUdpLen()  # number of bytes
    print("LENGTH: " + str(sender.udpL))

    keys = encrypt.readKeys("keyall1", 'rb')
    sender.info = encrypt.encrypt(sender.info, keys)
    sender.addpadding(sender.info)
    sender.check = sender.checksum()
    print("THE CHECK: " + str(sender.check))
    datag = sender.setDatagram()
    datag = sendMsg(datag)
    s.sendto(datag, (tempIP, sender.de_port))  # send the data
    # s.settimeout(2)  # wait for response

    response, addr = s.recvfrom(2056)
    response = response.decode('utf-8')
    print(response)
    s.close()
