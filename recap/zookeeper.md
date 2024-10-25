📚 **Class Recap: ZooKeeper**

Hey everyone! 👋 Here is what we discussed in the session today:

**Problem Statement: State Tracking**
- In a Master-Slave architecture, all writes must come to the master, requiring all clients to know the master's identity.
- If the master dies, a new master must be selected, and all machines should sync with this change.
- Using a single machine to track the master leads to a single point of failure and introduces an additional hop for every request.

🐅 **ZooKeeper**
- ZooKeeper tracks data in a strongly consistent form, organised like a file system with nodes (ZK nodes).
- Ephemeral Nodes: Valid only as long as the session/machine that wrote the data is alive.
- Persistent Nodes: Not deleted unless explicitly requested.

👑 **Master Election**
- Machines in a cluster write their IP addresses to an ephemeral ZK node. Only one machine's write will succeed, designating it as the master.
- Clients set a watch on this node to get notified of any changes, reducing the need for frequent checks.
- If the master dies, the ephemeral node is deleted, and all subscribers are notified.
- Slaves attempt to become the new master, and clients update their master reference accordingly.

🏛️ **Architecture**
- ZooKeeper operates with multiple machines (odd number) to avoid a single point of failure.
- Leader election among ZooKeeper machines ensures data consistency and fault tolerance.
- Majority acknowledgment (quorum) is required for write operations to prevent split-brain scenarios.