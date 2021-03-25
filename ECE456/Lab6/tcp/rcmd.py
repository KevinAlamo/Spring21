import socket
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) != 6:
        raise ValueError('Incorrect num of args')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    hostN = sys.argv[1]
    port = int(sys.argv[2])  # Reserve a port for your service.
    host = socket.gethostbyname(hostN)

    s.connect((host, port))
    execTime = sys.argv[3]
    delay = sys.argv[4]
    cmd = sys.argv[5]
    cmdToSend = execTime + "@" + delay + "@" + cmd + "@"

    s.send(bytes(cmdToSend.encode("ascii")))  # send the file name
    # time.sleep(3)
    filelen = s.recv(10)  # read length of message
    while filelen == b'':
        filelen = s.recv(10)
    filelen = filelen.decode("ascii")

    temp = s.recv(int(filelen))

    print(temp.decode("utf-8"))  # receive info
    s.close  # Close the socket when done
