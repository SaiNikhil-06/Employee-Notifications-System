import socket
import sys
import random
import os

from _thread import *
from threading import Timer

userList = []
Employeetopics = ['Technology','Finance','Marketing','Human Resources','Design','Operations']
topics = ['Human Resources','Design','Operations']

subscriptions = {}
generatedEvents = dict()
flags = dict()
events = { 'Human Resources' : ['The impact of remote work on employee engagement', 'Upcoming webinar on best practices for performance management','How to improve diversity and inclusion in your workplace','How to create effective onboarding programs for new employees'],
    'Design' : ['New design tools now available for creating interactive prototypes', 'The role of design in building brand identity and recognition','Case study: how we improved user engagement with redesign of our website','Upcoming workshop on design thinking and innovation'],
    'Operations' : ['How to streamline your supply chain for maximum efficiency','Upcoming webinar on the latest trends in logistics and transportation','The role of operations in sustainability and corporate social responsibility','How to create effective process improvement initiatives']
}

def threadedClient(connection, data):
    while True:
        flags[data] = 0
        subscribe(data)
        subscriptionInfo = 'Your subscriptions are : ' + str(subscriptions[data])
        connection.send(subscriptionInfo.encode())
        
        while True:
            if flags[data]==1:
                notify(connection,data)

    connection.close()

def threadedServerSender(connection, data):
    while True:
        flags[data] = 0
        subscriptions[data] = topics
        subscriptionInfo = 'Your topic subscriptions are : ' + str(subscriptions[data])
        connection.send(subscriptionInfo.encode())
        
        while True:
            if flags[data]==1:
                notify(connection,data)
    connection.close()

def threadedServerReceiver(connection, data):
    while True:
        serverData = connection.recv(2048).decode()
        m = serverData.split('-')
        if len(m)==2:
            topic = m[0]
            event = m[1]
            publish(topic,event,0)
    connection.close()

def threadedMasterSender(ss):
    while True:
        flags['master'] = 0
        subscriptions['master'] = topics
        subscriptionInfo = 'Your topic subscriptions are : ' + str(subscriptions['master'])
        ss.send(subscriptionInfo.encode())
        while True:
            if flags['master']==1:
                notify(ss,'master')
    ss.close()

def threadedMasterReceiver(ss):
    while True:
        serverData = ss.recv(2048).decode()
        if serverData:
            print("Received from MASTER :",serverData)
            p = serverData.split('-')
            if len(p)==2:
                topic = p[0]
                event = p[1]
                publish(topic,event,0)
    connection.close()


def subscribe(name):
    subscriptions[name] = ['Operations']

def eventGenerator():
    
    topic = random.choice(topics)
    msgList = events[topic]
    event = msgList[random.choice(list(range(1,len(msgList))))]
    publish(topic,event,1)


def publish(topic,event,indicator):
    
    event = topic + ' - ' + event
    if indicator == 1:
        for name, topics in subscriptions.items() :
            if topic in topics:
                if name in generatedEvents.keys():
                    generatedEvents[name].append(event)
                else:
                    generatedEvents.setdefault(name, []).append(event)
                flags[name] = 1

    else:
        for name, topics in subscriptions.items() :
            if name in userList:
                if topic in topics:
                    if name in generatedEvents.keys():
                        generatedEvents[name].append(event)
                    else:
                            generatedEvents.setdefault(name, []).append(event)
                    flags[name] = 1

    t = Timer(random.choice(list(range(30,36))), eventGenerator)
    t.start()


def notify(connection,name):
    if name in generatedEvents.keys():
        for msg in generatedEvents[name]:
            msg = msg  + str("\n")
            connection.send(msg.encode())
        del generatedEvents[name]
        flags[name] = 0


def Main():    
    host = ""
    port = 5043
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port))
    print("Socket is bind to the port :", port)
    s.listen(5)
    print("Socket is now listening for new connection ...")
    t = Timer(random.choice(list(range(30,36))), eventGenerator)
    t.start()

    master_host = os.environ.get("MASTER_HOST", 'server001')
    master_port =  5040

    serverName = str(sys.argv[1])
    
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.connect((master_host,master_port))
    
    ss.send(serverName.encode())
    
    start_new_thread(threadedMasterReceiver, (ss,))
    start_new_thread(threadedMasterSender, (ss,))
    
    while True:
        
        connection, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        #print("Connection string is",connection)
        
        data = connection.recv(2048).decode()
        
        if data:
            print("Welcome ",data)
        l = data.split('-')
        if l[0]=='c':
            userList.append(l[1])
            start_new_thread(threadedClient, (connection,l[1]))
        if l[0]=='s':
            start_new_thread(threadedServerSender, (connection,l[1]))
            start_new_thread(threadedServerReceiver, (connection,l[1]))

    s.close()

if __name__ == '__main__':
    Main()