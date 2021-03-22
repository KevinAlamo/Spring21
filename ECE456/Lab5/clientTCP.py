import socket
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Incorrect num of args')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = sys.argv[1]
    port = 5000  # Reserve a port for your service.

    s.connect((host, port))
    filename = sys.argv[2]
    f = open(filename, 'rb')
    filename = filename + '@'
    s.send(bytes(filename.encode()))  # send the file name
    # time.sleep(3)
    print('Sending...')
    dat = f.read(1024)
    while dat:
        print('Sending...')
        s.send(dat)
        dat = f.read(1024)
    f.close()
    print("Done Sending")
    print(s.recv(1024).decode("utf-8"))  # receive confirmation
    s.close  # Close the socket when done
