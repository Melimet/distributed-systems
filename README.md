# Distributed File System

#### Erkka Rahikainen, Valtteri Kodisto, Joni Taajamo

## Introduction

The aim of this project is to design and implement a distributed file system that is scalable, reliable, and maintains strong consistency while ensuring ease of deployment. The use case is similar to AWS S3, catering to large numbers of users storing vast amounts of data. In this architecture, the client communicates with a Distributed Hash Table (DHT, acting as a reverse proxy), which in turn interacts with distributed clusters responsible for storing files. Each file's root directory is associated with a hash key, assigning a specific cluster to a set of directories determined by the DHT. Each cluster has a leader and a follower (read replica) to provide redundancy in case the leader node fails.

## Architectural Overview

![Architecture](https://github.com/Melimet/distributed-systems/assets/33700058/b09cdb32-0776-4bf0-b06f-02bdd806f0f2)

### Client

The client initiates requests to the DHT, which then handles the responses.

### Distributed Hash Table (DHT)

The DHT is responsible for processing client requests, which are then forwarded to a specific cluster based on a hash key derived from the file directory targeted by the request. One of the DHTs acts as the leader, with the others as followers. When a new cluster is created, the leader DHT synchronizes the follower DHTs to reflect the updated hash table. This update is then synchronously processed on follower nodes before handling more requests.

### Clusters and Data Storage Nodes
![Node architecture](https://github.com/Melimet/distributed-systems/assets/33700058/1636c968-48d8-4a30-bac1-7a2fcf3ddbcb)

Clusters consist of a leader node and follower nodes. The leader node handles data operations (create, update, delete). Given the S3 use case's read-heavy nature, all followers can respond to read requests, while only the leader handles other data operations.

Clusters scale by "splitting" in half. When a new cluster is formed, the leader DHT updates the hash key address space. For example, if Cluster 1 initially managed hash keys 1-10, it might now handle keys 1-5, with Cluster 2 taking over keys 6-10. Initially, Cluster 2's state mirrors that of Cluster 1's database.

## Solution Techniques

### Logical Clock

Logical clocks ensure the order of operations within a cluster. Sequence IDs are requested from the leader node to maintain consistency among nodes.

### Synchronization

If a follower node falls out of sync, it's detected when the node requests the latest sequence ID from the leader. After a timeout, the follower sends a synchronization request to the leader to retrieve missing requests. Leader nodes store `x` number of latest requests for synchronization purposes. A leader node of a cluster will never be out of sync as it exclusively processes state-changing requests.

If a node lacks the missing requests, the requesting node discards its entire database and requests full synchronization from another node.

### Virtualization and Kubernetes

Virtualization and Kubernetes facilitate easy deployment, management, and scaling of the distributed file system.

### Redis

Redis enhances system performance, serving as a fast, scalable data store, potentially for caching frequently accessed data. In this solution, Redis is also used for long-term storage, utilizing its persistence features.

#### Messaging Between Nodes

## Description of Messages Sent and Received by Nodes

### Client - DHT
Involves basic API requests from the client, managed by the reverse proxy. Below is an example of a client requesting files within a specific file path.


```
SELECT
FILE_PATH
```

### DHT - Data Storage Node

Communication via sockets for forwarding client requests to the appropriate server cluster. Below is an example of a delete request between DHT and a data storage node.

```
DELETE
SEQUENCE_ID
FILE_PATH
```


### Data Storage Node - Data Storage Node

Socket-based communication for transmitting changes and ensuring consistency across nodes. Below is an example of an insert request between two data storage nodes.

```
INSERT
SEQUENCE_ID
FILE_PATH
DATA
```


## Features to Implement

We'll likely develop a Kubernetes solution with a single DHT capable of scaling up more file storage clusters based on demand. This approach will make the solution highly scalable, even though the DHT may become a bottleneck. The system is fault-tolerant, as file storage clusters have read replica backups from follower nodes in each cluster. However, the DHT is a single point of failure, as we might not have time to implement a multi-DHT solution. Synchronization is maintained within each cluster, with the leader node directing followers to update the state.

