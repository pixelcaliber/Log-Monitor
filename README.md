# Real-Time Log Monitoring and Broadcasting System
## Project Overview

This application is a robust, real-time log monitoring and broadcasting system. It leverages the power of asyncio, WebSockets, docker and load balancing through NGINX to create a scalable solution for monitoring vast size log files and broadcasting updates to multiple clients in real-time.


## Key Features

1. Real-time log file monitoring
2. WebSocket-based live updates to connected clients without them to refresh the page
3. Multithreaded architecture for improved performance and handling multiple clients
4. Load balancing to handle to distribute the load among the servers achieving scalability
5. System leverages containerization and load balancing to ensure high availability and scalability

## System Architecture

#### LogMonitor

The `LogMonitor` class is designed to continuously read from a specified log file present in remote server through docker bind mount, detecting new entries as they are appended. It implements the Observer pattern, allowing multiple listeners (such as the WebSocket server) to be notified of new log entries in real-time.

Key features:
- Efficient file reading using binary mode and seek operations
- Support for retrieving the last N lines of the log file
- Thread-safe observer registration and notification

#### Socket (WebSocket Server)

The `Socket` class manages WebSocket connections with clients, providing real-time updates of log changes. It's built on top of the `websockets` library, leveraging Python's asynchronous capabilities for high-performance communication through asyncio.

Key features:
- Asynchronous client handling for improved scalability
- Periodic client pinging to maintain connection integrity and freeing up space 

#### Flask Application

The Flask application serves as the main entry point and provides a RESTful API for interacting with the system. It's designed using the application factory pattern, allowing for easy configuration and extension.

## Performance and Scalability
The system has been designed and tested for high performance and scalability, check `load_test.py`:
### Load Testing Results
Load testing has been performed to ensure the system can handle a large number of concurrent connections:

- Concurrent Clients: Successfully tested with 1000 simultaneous client connections.
- Server Instances: The test was conducted with 30 application instances.
- Performance: The system maintained responsiveness and data integrity under this high load.

#### These results demonstrate the system's capability to handle a significant number of concurrent users, making it suitable for large-scale deployments.

## Approach and Design Principles

1. **Asynchronous Programming**: Leveraging async/await syntax for efficient I/O operations and client handling.

2. **Observer Pattern**: Implemented in the LogMonitor to allow flexible and decoupled event notification.

3. **Factory Pattern**: Used in the Flask application setup for improved configurability and testing.


### Commands
```
cd app
    python -m venv venv
    source venv/bin/active
    
    python test/load_test.py 
cd ..
```

### minikube commands:

```
brew install minikube
brew install docker
brew install docker-compose 

brew install qemu
    -> once qemu installed follow this page: 
        https://minikube.sigs.k8s.io/docs/drivers/qemu/ 
    and do the essentials to prevent the errors

minikube ip
minikube status
minikube start --driver qemu --network socket_vmnet --extra-config=kubelet.authorization-mode=AlwaysAllow
minikube delete
```

### docker commands
```
docker compose up --build -d --scale app=3 (any number of servers which you want)
docker ps --format '{{.Names}}' 
docker system prune -a

if getting docker-desktop config error, run -> 
    vi ~/.docker/config.json 

then, remove desktop credentials, file should be like this:
    {
            "auths": {},
            "experimental": "disabled"
    }
    
    
docker exec -it nginx /bin/bash

docker system prune -a --volume 
-> prune the entire docker system

docker images prune
docker volumes prune
```


### How to start?
```
 minikube start --driver qemu --network socket_vmnet --extra-config=kubelet.authorization-mode=AlwaysAllow
 -> start the minikube
 
minikube mount /Users/abhinavpandey/Downloads/practice/first/shared:/minikube-host
-> mount the file path to minikube-host 

docker compose up --build -d --scale app=10
-> start the container with number of pods of your choice


minikube ip
-> get the minikube

ws://<minikube-ip>/ws (eg: "ws://192.168.105.2/ws")
-> this the route to which we can connect using postman and get the updates
```

