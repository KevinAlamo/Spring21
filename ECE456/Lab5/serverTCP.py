import socket


if __name__ == '__main__':
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 5000                 # Reserve a port for your service.
    print(socket.gethostbyname(socket.gethostname()))
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        filename = c.recv(1024)  # read file name
        filename = filename.decode("utf-8")
        print("Receiving file", filename)
        f = open(filename, 'wb')
        dat = c.recv(1024)
        while (dat):
            print("Receiving...")
            f.write(dat)
            dat = c.recv(1024)
        f.close()
        print("Done Receiving")
        c.close()                # Close the connection
