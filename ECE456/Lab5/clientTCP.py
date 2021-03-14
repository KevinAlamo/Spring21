import socket
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Incorrect num of args')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = sys.argv[1]
    port = 5000  # Reserve a port for your service.

    s.connect((host, port))
    filename = sys.argv[2]
    s.send(bytes(filename))
    f = open(filename, 'rb')
    print('Sending...')
    dat = f.read(1024)
    while dat:
        print('Sending...')
        s.send(dat)
        dat = f.read(1024)
    f.close()
    print("Done Sending")
    print(s.recv(1024))
    s.close  # Close the socket when done
