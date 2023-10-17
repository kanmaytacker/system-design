# Zookeeper and Kafka

## Key terms

### Zookeeper

> ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

### Asynchronous processing
> Asynchronous processing is a method of working with a request where the client sends a request to the server and does not wait for the response. The client can continue to do other work while waiting for the response. When the response is ready, the server sends the response to the client.

## Zookeeper

### Motivation

Often, a single database server does not provide enough throughput or storage capacity for a given application. In such cases, it is necessary to partition the data across multiple servers. This partitioning is called sharding. Sharding introduces a new problem: how do you keep track of which server has which data? This problem is known as coordination.

Multiple servers are often structured in a master-slave configuration. This also introduces a problem when the master fails. How do you elect a new master? This problem is known as leader election.
   
![Master slave](https://repository-images.githubusercontent.com/497947677/65d4fb35-189e-4d9e-8be8-ada725cdf315)

You could start with a very simple approach of having a single server storing the data and metadata. This server would be a single point of failure. If this server fails, the entire system would be unavailable. You could add a second server to the system to act as a backup. This would solve the problem of availability, but it would introduce a new problem: how do you keep the two servers in sync? This problem is known as replication. The problems with this approach are:
1. `Single point of failure` - If the server fails, the entire system is unavailable.
2. `Additional hop` - For each request, the client has to make an additional hop to the server that stores the data.

To solve, the single point of failure, you could add a cluster of servers. This would solve the problem of availability, but it would introduce new problems as mentioned above. The problems with this approach are:
- `Master election` - How do you know which server is the master?
- `Replication` - How do you keep the servers in sync?
- `Reduce hops` - How do you reduce the number of hops for each request?

### Solution

Zookeeper follows the idea we discussed above. It is a cluster of servers that work together to provide a highly available service. It is used to solve the problems of coordination and leader election. It is used by many distributed systems such as Hadoop, HBase, Kafka, and many others.

Zookeeper is a centralised service that tracks data in a tree-like structure. Each node in the tree is called a znode. Each znode can have data associated with it. Zookeeper provides APIs to create, update, and delete znodes. Zookeeper also provides APIs to watch for changes to znodes. This is useful for coordination and leader election.

![Zookeeper](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmiro.medium.com%2Fmax%2F1400%2F0*dvXEiUvKqgPRLA1x.png&f=1&nofb=1&ipt=4502f2f79c5d1fa0eba9d0882c37790a87777f165322cbd95bdc7890ed520c79&ipo=images)

A ZK node can be of two types:
1. `Ephemeral` - The node is deleted when the client that created the node disconnects from the server.
2. `Persistent` - The node is not deleted when the client that created the node disconnects from the server.

### Leader election

Let's say that you have a cluster of servers and for now you have a single zookeeper node. There are three database servers `DB1`, `DB2` and `DB3`. Let's follow the steps below to see how leader election works:
1. Initially, there is no leader so all the servers are in the `LOOKING` state i.e. they are looking for a leader.
2. All these servers try to become the leader by sending a `leader election` request to the zookeeper node.
3. The zookeeper node has a `/master` znode. The first server to add its information to this znode becomes the leader.
4. Let's say that `DB1` is the first server to add its information to the `/master` znode. It becomes the leader and the other servers become followers.
5. The leader has to keep on emitting `heartbeat` messages to the zookeeper node. If the leader fails to do so, the zookeeper node will remove the leader from the `/master` znode.
6. If the leader fails, the value of the `/master` znode will change to null. The other servers will get notified of this change and they will try to become the leader and the process repeats.


### Zookeeper architecture and quorum

Zookeeper itself is a distributed system. It is a cluster of servers that work together to provide a highly available service. The servers in the cluster are called `ensemble`. The ensemble is responsible for storing the data and metadata. With multiple servers, zookeeper itself requires coordination and leader election. Zookeeper uses a modified version of the `Paxos` algorithm to solve this problem, known as `Zookeeper Atomic Broadcast` (ZAB).

To ensure strong consistency, zookeeper requires a majority of servers to be available. This is known as `quorum`. For example, if you have a cluster of 5 servers, you need at least 3 servers to be available to ensure strong consistency. This quorum is used for coordination and leader election. For any change to be made to the data or metadata, a majority of servers must agree on the change. This ensures that the data and metadata are consistent across all the servers. The transactions across zookeeper run as follows:

- Among the ensemble of servers, a server is elected as a leader, and all the remaining servers are made followers. The leader handles all requests and the followers receive the updates proposed by the leader.
- The ZooKeeper service takes care of replacing leaders on failures and syncing followers with leaders, and the whole process is fully transparent to client applications. The service relies on the replication mechanism to ensure that all updates are persistent in all the servers that constitute the ensemble.
- The ZooKeeper service takes care of replacing leaders on failures and syncing followers with leaders, and the whole process is fully transparent to client applications. The service relies on the replication mechanism to ensure that all updates are persistent in all the servers that constitute the ensemble.
- Read requests such as exists, getData, and getChildren are processed locally by the ZooKeeper server where the client is connected. This makes the read operations very fast in ZooKeeper. Write or update requests such as create, delete, and setData are forwarded to the leader in the ensemble. The leader carries out the client request as a transaction.

**Acknowledgment during Updates:**

When a client sends an update request to ZooKeeper, it is broadcasted to all nodes in the ensemble. For the update to be acknowledged:

1. **A quorum of nodes must acknowledge the update:** A quorum, which is a majority of the nodes in the ensemble, must acknowledge the update for it to be considered successful. If a majority of nodes confirm the update, ZooKeeper considers the operation successful, ensuring fault tolerance and data consistency.

2. **Write operation is committed:** Once the update is acknowledged by the required quorum, it is committed and becomes part of the ZooKeeper's data. Clients can trust that the data they write is safely stored and replicated across multiple nodes.

**Read Operation in ZooKeeper:**
When a client sends a read request to ZooKeeper:

1. **Querying all nodes is not necessary:** Unlike the update operation, the client does not need to query all nodes in the ensemble. Instead, the client sends the read request to any node in the ensemble.

2. **Consistent read from a single node:** The node receiving the read request checks if it is part of the quorum. If it is, it serves the read request. Since all nodes in the quorum have the same data (due to the acknowledgment process during updates), the client receives a consistent response regardless of which node it queries within the quorum.

3. **Ensuring consistency:** ZooKeeper ensures that if a read request is served by a node within the quorum, the client receives the latest committed version of the data. If the read request were served by a node outside the quorum, there would be a risk of reading stale or inconsistent data.

Let's consider a simple configuration scenario where a distributed application's configuration setting needs to be updated in a ZooKeeper ensemble with three nodes: Node A, Node B, and Node C.

**Initial Configuration State:**
- **Configuration Key:** `max_connections`
- **Initial Value:** `100`

**Update Request Process:**

1. **Client Sends an Update Request:**
   - The client wants to update the `max_connections` configuration setting to `150`.
   - The update request is sent to all nodes: Node A, Node B, and Node C.

2. **Acknowledgment and Quorum:**
   - For the update to be successful, a majority of nodes must acknowledge the change. In this case, it means at least two nodes (since there are three nodes in the ensemble) need to acknowledge the update.
   - If Node A and Node B acknowledge the update, a quorum is reached.

3. **Propagation of Update:**
   - The update is replicated to all nodes in the ensemble. In this case, Node A and Node B receive the update and apply it to their local copies of the data.
   - The quorum ensures that the update is applied to a majority of nodes, ensuring consistency and fault tolerance.

4. **Quorum Storage:**
   - The fact that Node A and Node B have acknowledged the update is stored persistently, ensuring that if a node restarts or fails, the quorum can be re-established based on the persistent storage.

**Read Request Process:**

1. **Client Sends a Read Request:**
   - Another client wants to read the `max_connections` configuration setting.
   - The read request is sent to any node in the ensemble. For this example, let's say the read request is sent to Node B.

2. **Serving the Read Request:**
   - Node B checks if it is part of the quorum that acknowledged the most recent update (which it is, as it acknowledged the update during the previous step).
   - Node B serves the read request and returns the value `150` to the client.
  
3. **Consistency Ensured:**
   - Because the client's read request was served by a node within the quorum, it receives the most recent and consistent value of `max_connections`, which is `150`.

**Important Points:**
- **Quorum Consistency:** Quorum ensures that updates are applied consistently to a majority of nodes before being considered successful. This consistency is maintained during updates and guarantees that reads will always return a consistent value from a node within the quorum.
  
- **Persistence:** Acknowledgments and quorum information are stored persistently on the nodes. This persistence ensures that if a node restarts, it can recover its previous state and participate in the quorum.

- **Dynamic Reconfiguration:** The ZooKeeper ensemble can be dynamically reconfigured. Nodes can be added or removed, but this process must be managed carefully to maintain the majority quorum and ensure continued consistency and fault tolerance.

## Kafka

### Motivation

In a real system such as an e-commerce application, an action can trigger multiple different processing steps. For example, when a user places an order, the following steps can be triggered:
1. Send an email to the user.
2. Send a notification to the user's mobile device.
3. Update the inventory.
4. Update the user's order history.
5. Update the user's profile.
6. Update the user's loyalty points.

Expecting the user to wait for all these steps to complete is neither a good idea nor feasible. The user will have to wait for a long time before the order is placed. This is where asynchronous processing comes into the picture. Let us see how asynchronous processing works:

1. The user places an order.
2. The order is added to a queue.
3. The user is notified that the order has been placed.
4. Behind the scenes, the order is processed asynchronously.
5. The order is picked up from the queue and processed by different services.

![Asynchronous processing](https://miro.medium.com/v2/resize:fit:2000/1*dvJJTF-M3QNU7ra_QJwz2A.png)

An asynchronous pipeline backed by a message queue solves our problem. It allows us to process the order asynchronously. It also allows us to scale the system by adding more consumers to the queue. There are two types of message queues:
- `Push queues` - The producer pushes the message to the queue and the consumer is notified of the message e.g. SNS
- `Pull queues` - The producer pushes the message to the queue and the consumer pulls the message from the queue e.g. SQS, Kafka

Push queues use a pub-sub model where the producer publishes the message to a topic and the consumer subscribes to the topic. Pull queues use a point-to-point model where the producer pushes the message to a queue and the consumer pulls the message from the queue.

A problem associated with queues comes up when the queue goes down. If the queue was full, and it goes down all the messages in the queue will be lost.

### Solution - Persistent queues
This is where Kafka comes into the picture. Kafka is a distributed streaming platform that solves this problem. Kafka is a distributed system that runs as a cluster of servers. It is a distributed commit log that allows you to store and process streams of records in real-time.  Persistent queues are queues that store the messages on disk using the commit log pattern.

Following are the key concepts in Kafka:
1. `Publisher` - A publisher pushes messages to the queue. These messages are the actions that need to be processed such as placing an order.
2. `Subscriber` - A subscriber is a consumer that pulls messages from the queue. These messages are the actions that need to be processed such as sending an email, sending a notification, updating the inventory, etc.
3. `Topics` - A topic is a category or feed name to which messages are published. Topics help us segregate messages based on the type of action that needs to be performed. For example, we can have a topic for sending emails, a topic for sending notifications, a topic for updating the inventory, etc.
4. `Broker` - A broker is a server that runs as part of a Kafka cluster. It stores the messages in the queue. It also provides APIs to publish and consume messages.

#### Partitioning

Kafka is a high-throughput system. It can handle millions of messages per second. To achieve this, Kafka partitions the data across multiple servers. This is known as partitioning. Each partition is stored on a different server. This allows Kafka to scale horizontally by storing messages on different servers. 

![Partitioning](https://daxg39y63pxwu.cloudfront.net/images/blog/apache-kafka-architecture-/image_589142173211625734253276.png)

Kafka either partitions messages by a key or by round-robin. If the messages are partitioned by a key, all the messages with the same key will be stored in the same partition. If the messages are partitioned by round-robin, the messages will be distributed across all the partitions in a round-robin fashion. They key is defined by the publisher.

**Consumer Groups**
Kafka consumers can be organized into consumer groups. Each message in a partition is delivered to only one consumer within a consumer group. If multiple consumers belong to the same consumer group and subscribe to the same partition, Kafka ensures that each message is processed by only one consumer in that group.

**Offset Management**
Each consumer in a consumer group keeps track of its progress in the partition by maintaining an offset, which is the position of the last message it has consumed. Kafka ensures that each message is delivered to consumers only once by managing these offsets.
When a consumer processes a message, it updates its offset. If a consumer fails and restarts, it can resume processing from the last offset it committed, ensuring that it does not reprocess messages.

**Message Acknowledgment**
Kafka supports message acknowledgment. Once a message is successfully processed, the consumer acknowledges the message. Acknowledgment indicates that the message has been processed and can be safely marked as consumed.
If a consumer fails before acknowledging a message, Kafka can redeliver the message to another consumer in the same consumer group, ensuring that the message is processed even if one consumer fails.

### Additional reading
- [Zookeeper Internals](https://zookeeper.apache.org/doc/r3.4.13/zookeeperInternals.html)
- [ZAB vs Paxos](https://cwiki.apache.org/confluence/display/ZOOKEEPER/Zab+vs.+Paxos)
- [How is a leader elected](https://www.quora.com/How-is-a-leader-elected-in-Apache-ZooKeeper)
- [Offsets in Kafka](https://dattell.com/data-architecture-blog/understanding-kafka-consumer-offset/)