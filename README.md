# Distributed file system
#### Erkka Rahikainen, Valtteri Kodisto, Joni Taajamo

The goal of this project is to design and implement a distributed file system which is scalable, fault-tolerant and consistent. 
Briefly, the architecture of this solution is a Client-Proxy-Nodes Architecture. The client sends requests to the proxy, which then forwards the request to a chosen node. The nodes are responsible for storing the files and broadcasting changes to other nodes. The nodes are also responsible for handling the requests from the proxy. The proxy is responsible for handling the requests from the client and forwarding them to the correct node. The client is responsible for sending requests to the proxy and handling the responses from the proxy.


## More indepth description of the topic and selected solution techniques

### Reverse proxy

### Sequencing

### Virtualization and Kubernetes

### Redis

### 



## Description of different nodes

### Client

### Reverse proxy

#### Discovery

#### Load balancing

#### Sequencing

### File server
#### Broadcasting to other nodes


## Description of messages sent and received by nodes

### Client - Reverse proxy - Basic api requests

###  Reverse proxy - File server - sockets

###  File server - file server - sockets

## Features to implement

### Scalability aspects

### Fault tolerance

### Node discovery

### Synchronization and consistency

### Consensus