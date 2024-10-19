# Zookeeper

## Setup
### Docker Compose
To start Zookeeper with Docker Compose, use the following command:

```bash
docker-compose up -d
```
To verify that the Zookeeper container is running, you can use the following command:

```bash
docker-compose ps
```
### Zookeeper CLI
Connect to the running Zookeeper container using:

```bash
docker exec -it zookeeper /bin/bash
```

Start the Zookeeper CLI to connect to the running Zookeeper instance:

```bash
bin/zkCli.sh
```

---
## Centralised configuration management

In distributed systems, you often need a **centralised place to store configuration** so all services have a consistent set of parameters.
Zookeeper can act as this central store, allowing you to change configurations dynamically and have services respond in real-time.


1. Create the configuration node

    ```bash
    create /config ""
    [zk] Created /config
    ```
2. Create an ephemeral node for the database configuration

    ```bash
    create -e /config/database "db_host=localhost;db_port=5432"
    ```
3.  Any service can retrieve the configuration data from Zookeeper.

    ```bash
    get /config/database
    ```

    Output:

    ```bash
    db_host=localhost;db_port=5432
    ```
4. **Watch for Configuration Changes**: Set a watch on the configuration node so services get notified when the configuration changes.
    ```bash
    get /config/database -w
    ```

5. Now, in another terminal, simulate a configuration change.
    > You can connect using `docker exec -it zookeeper /bin/zkCli.sh` and run the following command:
    
    ```bash
    set /config/database "db_host=localhost;db_port=5433"
    ```
6. The service will receive a notification of the configuration change.

    ```bash
    WatchedEvent state:SyncConnected type:NodeDataChanged path:/config/database
    ```
---
## Leader Election

Leader election is crucial in systems where one node must act as the leader or **master** (e.g., in a **failover scenario** when the master goes down).
Zookeeper can be used to dynamically elect a leader among multiple candidates.

You can use the sequential znodes to implement leader election.
They are created under a common parent node, and the node with the **lowest sequential number** becomes the leader.

### Steps:

1. **Leader Election Candidates Register**: Each candidate registers by creating an ephemeral sequential node under `/election`.

    ```bash
    create /election ""
    create -e -s /election/candidate "service1"
    create -e -s /election/candidate "service2"
    create -e -s /election/candidate "service3"
    ```

2. **Electing the Leader**: The node with the lowest sequential number becomes the leader. List the nodes under `/election`.

    ```bash
    ls /election
    ```

    Output:
    
    ```bash
    [candidate0000000000, candidate0000000001, candidate0000000002]
    ```

    The leader is the node with the smallest number:
    
    ```bash
    get /election/candidate0000000000
    ```

    Output:
    
    ```bash
    service1
    ```

   If `service1` disconnects (i.e., the master goes down), Zookeeper automatically deletes its node, and the next candidate (`service2`) becomes the leader.


3. **Clients Query the Leader for Writes**: Clients can query Zookeeper to discover the current leader (master) for write operations.

   ```bash
   get /election/candidate0000000000
   ```

   If the master fails, clients query again, and the new leader will take over.

---

> If you'd like to see how you can integrate Zookeeper programmatically, check out the script [here](./zoo.py).