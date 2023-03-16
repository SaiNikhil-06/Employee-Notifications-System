## The Following are used to import various that we can use in the application.
import sys
import socket

##declares a function called Main
'''
The code defines a function named "Main" which does not take any arguments.
It sets some variables, including the host and port that the client will connect to, as well as the name of the subscriber (which is obtained from the command line arguments passed to the script).
It creates a new socket using the AF_INET (IPv4) address family and the SOCK_STREAM socket type.
It connects to the server using the host and port specified earlier.
It enters into a loop where it repeatedly receives data from the server and prints it to the console.
In the first iteration of the loop, it sends the subscriber name to the server.
The data received from the server is decoded from bytes to a string using the decode() method and printed to the console using the print() function
'''
def Main():
    host = 'server002'
    port =  5041
    subscriberName = str(sys.argv[1])
    print("Subscriber is :",subscriberName)
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.connect((host,port))
    flag = True
    while True:
        if flag:
            soc.send(subscriberName.encode())
            flag = False
        data = soc.recv(2048).decode()
        print(data)

##This code assumes that the server is already running and listening on the specified host and port. It also assumes that the server and client are using the same protocol for sending and receiving data
if __name__ == '__main__':
    Main() ##Calling the main fuction
