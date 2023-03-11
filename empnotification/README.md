# Employee Notifications Publisher-Subscriber Distributed System

Employee Notification System -- Final project for distributed systems class: COEN 317 at Santa Clara University

Team members: Sai Nikhil Katara (W1653726) Vishnu Vardhan Kathika (W1630914) Sonam Yedge (W1632277)

The purpose of this project is to use the publisher subscriber model to provide all Employees with the updates and highlights of notifications for the specific topics. Users will be able to subscribe to a certain type of news or a specific topic of news. The publisher will retrieve the latest news data from the internet. On a regular basis, the publisher will provide a list of the latest news.

'Pub/sub' systems use an intermediary to distribute events to numerous receivers (called subscribers).  We'll use Docker containers to simulate a pub/sub system in this project.

Technologies used:
Python 
Node.js
Docker
To install follow the steps given here https://docs.docker.com/get-docker/

```
$ docker --version   #checking if docker is installed perfectly
```

## Frontend

First go the `empnotifications` directory. Then run the below commands:

```
docker build -t empnotification-image:v1 . #create new image for empnotification application
docker run -d -p 80:80 --name empnotification_central empnotification-image:v1
```

The application should be running on `https:\\localhost:80 `

## Backend 

Go the `empnotifications` directory. Then run the below commands:

```
docker-compose up
```


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
