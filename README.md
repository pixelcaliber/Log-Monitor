# Log-Monitor

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

