# The below modules are imported to make them work within the application
import socket
import sys
import random

from _thread import *
from threading import Timer

userList = []
Employeetopics = ['Technology','Finance','Marketing','Human Resources','Design','Operations']
topics = ['Technology','Finance','Marketing']
subscriptions = {}
events = { 'Technology' : ['New artificial intelligence tool now available for data analysis', '5 reasons why you should use cloud computing in your business', 'Upcoming webinar on the latest trends in software development','How blockchain is revolutionizing supply chain management'],
    'Finance' : ['Stock market report: record highs for tech companies', 'How to make the most of your retirement savings','Upcoming conference on investment opportunities in emerging markets','The importance of financial planning for small businesses'],
    'Marketing' : ['How to create an effective social media marketing strategy','New trends in influencer marketing you need to know about','Upcoming conference on the future of digital marketing','The role of customer experience in brand loyalty']
}

generatedEvents = dict()
flags = dict()
##This code defines a function named "threadedClient" that continuously sends subscription information to a client over a network connection and notifies the client whenever there is new data available based on flags set in the subscriptions dictionary until the connection is closed.
def threadedClient(connection, data):
    while True:
        flags[data] = 0
        subscribe(data)
        subscriptionInfo = 'Your topic subscriptions are : ' + str(subscriptions[data])
        connection.send(subscriptionInfo.encode())

        while True:
            if flags[data]==1:
                notify(connection,data)
    connection.close()

##This code defines a function that sends subscription information to a client over a connection and waits for notifications related to the subscription to be received, which it then sends to the client.
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

##This code defines a function named "threadedServerReceiver" that continuously receives data from a server through a connection and publishes it to a specified topic and event using another function named "publish".
def threadedServerReceiver(connection, data):
    while True:
        serverData = connection.recv(2048).decode()
        m = serverData.split('-')
        if len(m)==2:
            topic = m[0]
            event = m[1]
            publish(topic,event,0)
    connection.close()

def threadedServerReceiver(connection, data, server_id, neighbors):
    global currentLeader
    while True:
        serverData = connection.recv(2048).decode()
        m = serverData.split("-")

        if len(m) == 2:
            if m[0] == "leader":
                print(f"Server {server_id} received leader election message: {m}")
                received_priority = int(m[1])

                if received_priority != server_id:
                    if received_priority > currentLeader:
                        currentLeader = received_priority

                    # Forward the election message to the next server in the neighbors list
                    next_server = neighbors[server_id]
                    next_server.send(serverData.encode())

                if received_priority == currentLeader:
                    print(f"Server {server_id} elected as a leader")

            else:
                topic = m[0]
                event = m[1]
                publish(topic, event, e)

import time


def threadedServerSender(connection, server_id, neighbors):
    global currentLeader
    while True:
        # Initiating the leader election process
        if currentLeader is None:
            print(f"Server {server_id} initiating leader election")
            election_message = f"leader-{server_id}"
            next_server = neighbors[server_id]
            next_server.send(election_message.encode())
            time.sleep(2)  # Sleep for 2 seconds before the next iteration

        # Sending published events
        else:
            # Randomly select a topic and an event
            topic, event = get_random_topic_and_event()

            # Send the event to the current leader
            event_message = f"{topic}-{event}"
            leader_connection = neighbors[currentLeader]
            leader_connection.send(event_message.encode())
            time.sleep(5) 

def get_random_topic_and_event():
    # Define your own logic for selecting a random topic and event
    # For demonstration purposes, we will u‹se dummy values
    topics = ["Finance", "Human Resources", "Design", "Operations", "Technology"]
    events = ["Update 1", "Update 2", "Update 3"]

    import random
    topic = random.choice(topics)
    event = random.choice(events)

    return topic, event
def subscribe(name):
    subscriptions[name] = ['Finance']

##This code defines a function called "eventGenerator" that selects a random topic from a list of topics, selects a random message related to that topic, and publishes it to a messaging system with a message quality of 1.
def eventGenerator():
    
    topic = random.choice(topics)
    msgList = events[topic]
    event = msgList[random.choice(list(range(1,len(msgList))))]
    
    publish(topic,event,1)

##The code defines a function "publish" that generates and distributes events to subscribed clients, and schedules a new event generation timer.
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
            if name in userList: # only for clients
                if topic in topics:
                    if name in generatedEvents.keys():
                        generatedEvents[name].append(event)
                    else:
                        generatedEvents.setdefault(name, []).append(event)
                    flags[name] = 1

    t = Timer(random.choice(list(range(20,26))), eventGenerator)
    t.start()

##This code sends notifications of generated events to a specified connection for a given event name, then removes the event from the list of generated events and sets the corresponding flag to 0.                
def notify(connection,name):
    if name in generatedEvents.keys():
        for msg in generatedEvents[name]:
            msg = msg  + str("\n")
            connection.send(msg.encode())
        del generatedEvents[name]
        flags[name] = 0
##This is the main function that is going to be executed
def Main():
    
    host = "" 
    port = 5040
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port))
    print("Socket is bind to the port :", port)
    s.listen(5)
    print("Socket is now listening for new connection ...")
    
    t = Timer(random.choice(list(range(20,26))), eventGenerator)
    t.start()
##This code creates a server that listens for incoming client connections, receives messages from clients, and spawns threads to handle sending and receiving messages between clients.
    while True:
        
        connection, addr = s.accept() 
        print('Connected to :', addr[0], ':', addr[1])
        data = connection.recv(2048).decode()

        if data:
            print("Welcome ", data)
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
