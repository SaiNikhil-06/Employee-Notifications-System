## we had imported various modules inside the application 
import socket
import sys
import random

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
##This code defines a function that handles a threaded client connection and continuously subscribes to updates for a specified data, notifying the client when an update is received.
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
##This is a threaded server function that sends subscription information to a client and waits for notifications on the specified topics.
def threadedServerSender(connection, data):
    while True:
        flags[data] = 0
        subscriptions[data] = topics
        subscriptionInfo = 'Your subscriptions are : ' + str(subscriptions[data])
        connection.send(subscriptionInfo.encode())
        
        while True:
            if flags[data]==1:
                notify(connection,data)
    connection.close()

def threadedServerReceiver(connection, data):
    while True:
        serverData = connection.recv(2048).decode()
        m1= serverData.split('-')
        if len(m1)==2:
            topic = m1[0]
            event = m1[1]
            publish(topic,event,0)
    connection.close()
##This code defines a function that continuously sends a message containing a list of subscribed topics to a socket, and waits for a notification to send a message to the same socket.
def threadedMasterSender(ss):
    while True:
        flags['master'] = 0
        subscriptions['master'] = topics
        subscriptionInfo = 'Your subscriptions are : ' + str(subscriptions['master'])
        ss.send(subscriptionInfo.encode())
        while True:
            if flags['master']==1:
                notify(ss,'master')
    ss.close()

##This code defines a function that continuously receives data from a server, splits the data into topic and event, and publishes the event to subscribers of the given topic.
def threadedMasterReceiver(ss):
    while True:
        serverD = ss.recv(2048).decode()
        if serverD:
            print("Received from MASTER :",serverD)
            p = serverD.split('-')
            if len(p)==2:
                topic = p[0]
                event = p[1]
                publish(topic,event,0)
    connection.close()


def subscribe(name):
    subscriptions[name] = ['Design','Operations']

##This code defines a function that randomly selects a topic from a list, then randomly selects an event message from the corresponding list of events for that topic, and publishes the event with a quality of service of 1.
def eventGenerator():
    
    topic1 = random.choice(topics)

    msgList = events[topic1]

    event = msgList[random.choice(list(range(1,len(msgList))))]

    publish(topic1,event,1)


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

##This Dockerfile specifies a Python 3.6.4-slim base image, copies the current directory into a new directory called "server02" inside the container, sets the default command to run "pub_sub_s2.py" with the argument "s-server2" using Python, and exposes port 5041 for the container.
def notify(connection,name):
    if name in generatedEvents.keys():
        for msg in generatedEvents[name]:
            msg = msg  + str("\n")
            connection.send(msg.encode())
        del generatedEvents[name]
        flags[name] = 0

#The Below function is the main that is goiing to execute the whole function
def Main():    
    host = ""
    port = 5041
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port))
    print("Socket is bind to the port :", port)
    s.listen(5)
    print("Socket is now listening for new connection ...")
    t = Timer(random.choice(list(range(30,36))), eventGenerator)
    t.start()

    master_host = 'server001'
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