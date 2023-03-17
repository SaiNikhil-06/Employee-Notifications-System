## The Following are used to import various modules that we can use in the application.
import sys
import socket
import os

##declares a function called Main
def Main():
<<<<<<< HEAD

   
    host = os.environ.get("SERVER_HOST", "server001")  # Change this line
=======
    host = os.environ.get("SERVER_HOST", "server001") 
>>>>>>> 925f743 (Changes)
    port =  5040 
    subscriberName = str(sys.argv[1])
    print("Subscriber is :",subscriberName) 
    ##This line prints a message to the console indicating the name of the subscriber.
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ##This line creates a new socket object s using the TCP/IP protocol
    soc.connect((host,port))
    ##This line establishes a connection to the server at the specified host and port
    flag = True
    while True:
        if flag:
            soc.send(subscriberName.encode())
            flag = False
        data = soc.recv(2048).decode()
        print(data)
##Overall, this code sets up a client to connect to a server over TCP/IP using sockets, sends the subscriber's name to the server, and receives messages from the server to be printed to the console.
if __name__ == '__main__':
    Main()
