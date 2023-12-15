# Project report

Authors: Erkka Rahikainen, Valtteri Kodisto, Joni Taajamo

## Goals and Functionality:

Goal: Design and implement a scalable, reliable, and strongly consistent distributed file system (DFS) for large-scale data storage.

Core Functionality:
* Store and retrieve files across a distributed network of nodes.
* Handle read-heavy workloads efficiently.
* Maintain data consistency and fault tolerance.
* Ensure ease of deployment and management.

## Design Principles:

Architecture: Client-server architecture with three components:

* Client: Initiates file operations through a user-friendly API.
* Distributed Hash Table (DHT): Acts as a reverse proxy, mapping file paths to clusters based on hash keys and managing cluster scaling.
* Data Storage Clusters: Consist of leader and follower nodes. Leader handles write operations and maintains sequence IDs for consistency. Followers provide read redundancy and efficient data access.
Process: Requests flow from client to DHT to clusters and back. Leader node processes write requests and synchronizes followers.
Communication: Sockets for inter-node communication (client-DHT, DHT-cluster, cluster-cluster).

## Functionalities Provided:

* Naming and Node Discovery: DHT manages file location based on hash keys and dynamically discovers new nodes for cluster scaling.
* Consistency and Synchronization: Leader-follower approach with sequence IDs ensures consistent data across nodes. Leader maintains a history of recent requests for follower synchronization.
* Fault Tolerance and Recovery: Clusters remain operational even with follower failures. Full synchronization from another node or leader re-election recovers from leader failure.
* Scalability: Clusters can be split or joined based on load, with DHT managing the updated hash table and directing clients to appropriate clusters.

## Scalability Demonstration:

Cluster splitting allows adding new nodes for increased storage capacity and throughput.
DHT can manage multiple clusters, effectively distributing load and handling large-scale deployments.
Microservices architecture facilitates independent scaling of different system components.

## Key Enablers and Lessons Learned:

Enablers: Efficient data structures (hash tables), fault-tolerant protocols (leader-follower), containerization (Kubernetes) for easy deployment and scalability.
Lessons Learned: Importance of thorough testing for fault tolerance and consistency, choosing appropriate data storage solutions, considering potential bottlenecks (e.g., single DHT).
Test Driven Development would be key to success, and lacking test suite makes the development cumbersome.

## Group Member Participation:

Division of Tasks: All members contributed to design, implementation, testing, and report writing, with individual strengths leveraged.
Workload Distribution: Estimated as 35% Erkka Rahikainen, 35% Valtteri Kodisto, 30% Joni Taajamo, reflecting varying work hours and task complexity.
