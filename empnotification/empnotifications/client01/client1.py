import sys
import socket

def Main():
    host = 'server001'
    port =  5040 
    subscriberName = str(sys.argv[1])
    print("Subscriber is :",subscriberName) 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    flag = True
    while True:
        if flag:
            s.send(subscriberName.encode())
            flag = False
        data = s.recv(2048).decode()
        print(data)

if __name__ == '__main__':
    Main() 
