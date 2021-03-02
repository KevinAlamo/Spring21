import socket
import sys
from ECE456.Lab2 import receiver

if __name__ == '__main__':
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    receiver.sIP = socket.gethostbyname(socket.gethostname())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()  # accept new connection
    receiver.dIP = address
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 250 bytes
        data = conn.recv(250).decode()
        if not data:
            conn.close()
            conn, address = server_socket.accept()
            receiver.dIP = address
            # if data is not received break
            # break
        else:
            print("from connected user: " + str(data))



            data = input(' -> ')
            conn.send(data.encode())  # send data to the client

    # conn.close()  # close the connection

