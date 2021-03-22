import socket
import sys
import subprocess


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Incorrect num of args')

    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = int(sys.argv[1])                 # Reserve a port for your service.
    print(socket.gethostbyname(socket.gethostname()))
    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        print("Receiving command")

        f = open("tempfile.txt", 'wb')

        # import subprocess
        #
        # p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # print  "Today is", output
        cmd = c.recv(1024)
        cmd = cmd.decode("ascii")

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        for c in output:
            f.write(bytes(c, "utf-8"))


        f.close()
        print("Done Receiving")
        c.send("Successful Transfer".encode())
        c.close()                # Close the connection
