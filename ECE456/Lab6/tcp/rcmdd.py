import socket
import sys
import subprocess
import time

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
        print("Status = Connected")
        print("Receiving command")

        f = open("tempfile.txt", 'wb')

        cmd = c.recv(1024)
        cmd = cmd.decode("ascii")
        cmdArr = ["", "", ""]  # execTimes, execDelay, cmd
        tempCnt = 0
        for x in cmd:
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
            for cha in output:
                f.write(bytes(cha, "ascii"))

            f.write(bytes('\n', "ascii"))
            time.sleep(int(cmdArr[1]))

        f.close()
        toSend = ''
        f = open("tempfile.txt", 'rb')
        while (True):
            d = f.read(2)
            if d == b'':
                break
            toSend += d.decode("utf-8")
        sizeToSend = str(len(toSend))
        while len(sizeToSend.encode("ascii")) < 10:
            sizeToSend += " "

        c.send(sizeToSend.encode("ascii"))
        c.send(toSend.encode("utf-8"))
        print("Done Receiving")
        print("Status = Disconnected")
        c.close()                # Close the connection
