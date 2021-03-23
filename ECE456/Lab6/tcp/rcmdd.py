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
        print("Receiving command")

        f = open("tempfile.txt", 'wb')

        # import subprocess
        #
        # p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
        # (output, err) = p.communicate()
        # print  "Today is", output
        cmd = c.recv(1024)
        cmd = cmd.decode("ascii")
        cmdArr = ["", "", ""]  # execTimes, execDelay, cmd
        tempCnt = 0
        for x in cmd:
            if x == '@':
                tempCnt = tempCnt + 1
            if tempCnt == 3:
                break
            cmdArr[tempCnt] = cmdArr[tempCnt] + x

        for i in range(0, int(cmdArr[0])):
            p = subprocess.Popen(cmdArr[2], stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            output = str(output)
            for c in output:
                f.write(bytes(c, "ascii"))

            f.write(bytes('\n', "ascii"))
            time.sleep(cmdArr[1])

        f.close()
        f = open("tempfile.txt", 'rb')

        print("Done Receiving")
        c.send("Successful Transfer".encode())
        c.close()                # Close the connection
