import socket
import sys
from ECE456.Lab2 import receiver
import time

def sendMsg(msgs):
    res = ''
    for msg in msgs:
        res = res + msg

    return res
# -i scp command, client

def prepdata(data):
    prev = 0
    res = []
    num = 0
    s = b''
    for i in data:
        temp = bytes([i])
        s = b''.join([s, temp])
        if num == 1:
            res.append(s)
            num = 0
            s = b''
        else:
            num = num+1

    return res


if __name__ == '__main__':
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    receiver.dIP = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print(receiver.dIP)
    receiver.dIP = receiver.processIP(receiver.dIP)
    msgs = ['','','','', '']  # 5 msgs total
    i = 0
    receiver.keys = receiver.decrypt.readKeys('../Lab4/keyall1', 'rb')
    while True:
        # receive data stream. it won't accept data packet greater than 250 bytes
        rcvdata, address = server_socket.recvfrom(250)  # accept new connection
        receiver.sIP = address
        print("Connection from: " + str(address))
        if not rcvdata:

            rcvdata, address = server_socket.recvfrom(250)
            receiver.sIP = address
            # if data is not received break
            # break
        else:
            print("from connected user: " + str(rcvdata))

            receiver.sIP = receiver.processIP(receiver.sIP[0])
            tempIP = address[0]
            # grabbing data
            receiver.data = rcvdata
            receiver.data = prepdata(receiver.data)

            receiver.f = receiver.decrypt.decrypt(receiver.data[4:], receiver.keys)
            # getting udp header
            # so_port = data[0]
            # de_port = data[1]
            receiver.udpL = receiver.data[2]
            # check = data[3]
            receiver.checksum()
            receiver.removepadding(receiver.f)

            if i == 5:
                i = 0
            msgs[i] = "\nFrom IP: {ip} at time: {t}\n".format(ip=tempIP, t=time.time())
            for x in receiver.f:
                msgs[i] = msgs[i] + x.decode("utf-8")

            data = sendMsg(msgs)
            print(data)
            i = i + 1
            test = address[1]
            test2 = str.encode(data)
            test3 = str(port)
            server_socket.sendto(str.encode(data), (tempIP, address[1]))  # send data to the client

    # conn.close()  # close the connection

