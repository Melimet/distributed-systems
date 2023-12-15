# Project report

Authors: Erkka Rahikainen, Valtteri Kodisto, Joni Taajamo

## Goals and Functionality

Goal: Design and implement a scalable, reliable, and strongly consistent distributed file system (DFS) for large-scale data storage.

Core Functionality:
* Store and retrieve files across a distributed network of nodes.
* Handle read-heavy workloads efficiently.
* Maintain data consistency and fault tolerance.
* Ensure ease of deployment and management.

## Design Principles

Architecture: Client-server architecture with three main components: client, reverse-proxy & storage-node.

Client initiates file operations through a user-friendly API. Diverging from the plan, we decided to implement node registry on reverse-proxy, which maintains node metadata and leader-information. Data Storage nodes consist of leader and follower nodes. Leader handles write operations and maintains sequence IDs for consistency. Followers provide read redundancy and efficient data access. Requests flow from client to reverese-proxy to node and back. Leader node processes write requests and synchronizes followers. Sockets are used for inter-node communication (client<->reverese-proxy, reverese-proxy<->storage-node, storage-node<->storage-node).

System uses logical clock to keep track of mutation operations, incrementing it by one.

Using reverse-proxy for maintaining leader information becomes a single point failure, which is hard to avoid.

## Functionalities Provided

* Naming and Node Discovery: reverse-proxy manages file location based on hash keys and dynamically discovers new nodes for storage-node scaling.
* Consistency and Synchronization: Leader-follower approach with sequence IDs ensures consistent data across nodes. Leader maintains a history of recent requests for follower synchronization.
* Fault Tolerance and Recovery: Storage-nodes remain operational even with follower failures. Full synchronization from another node or leader re-election recovers from leader failure.
* Scalability: Storage-nodes can be split or joined based on load, with reverse-proxy managing the updated node registry and directing clients to appropriate node.

## Scalability Demonstration

Reverse-proxy can manage multiple storage-node, effectively distributing load and handling large-scale deployments.
Microservices architecture facilitates independent scaling of different system components.

## Key Enablers and Lessons Learned

Fault-tolerant protocols (leader-follower), containerization for easy deployment and scalability. Importance of thorough testing for fault tolerance and consistency, choosing appropriate data storage solutions, considering potential bottlenecks (e.g., single DHT). Test Driven Development would be key to success, and lacking test suite makes the development cumbersome.

## Group Member Participation

Division of Tasks: All members contributed to design, implementation, testing, and report writing, with individual strengths leveraged.
Workload Distribution: Estimated as 35% Erkka Rahikainen, 35% Valtteri Kodisto, 30% Joni Taajamo, reflecting varying work hours and task complexity.
