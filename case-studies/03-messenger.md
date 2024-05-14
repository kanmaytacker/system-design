# Facebook messenger case study

## Requirements

```
- User should be able to send messages to other users
- The messages should be delivered in real-time
- The user should be able to see a message history with other users
- The user should be able to see a list of the most recent conversations
```

## Back of the envelope calculations

**Task** - Come up with a basic data schema for the messenger app

### Entities and attributes

List all the entities that you think are necessary for the messenger app

```
- User
    - user_id
    - name
    - email
    - phone
- Conversation
    - conversation_id
    - user1_id
    - user2_id
- Message
    - message_id
    - conversation_id
    - sender_id
    - receiver_id
    - message
    - timestamp
```

### Estimations


**Question**: `What according to you would be the number of daily active users for the messenger app?`

**Answer**: `500 million`

**Question**: `How many conversations do you think a user would have in a day?`

**Answer**: `5`

**Question**: `How many messages do you think would be exchanged in a conversation?`

**Answer**: `10`

**Question**: `What are the total number of messages exchanged in a day?`

**Answer**: `500 million * 5 * 10 = 25 billion`

**Question**: `What is the size of a message?`

**Answer**: `200 bytes`

**Question**: `What is the total amount of data exchanged in a day?`

**Answer**: `25 billion * 200 bytes = 5 TB`

## Major operations

**Think of the different screens in the messenger app and the backend APIs that would be required to support them**

Screen - **Home screen**
API calls - 
```
- getRecentConversations(user_id)
```

Screen - **Chat screen**
```
- getMessages(conversation_id, user_id, limit, offset)
- sendMessage(conversation_id, sender_id, message)
```

---
## Design decisions

**Question**: `Will your system be read-heavy or write-heavy?`

**Answer**: `Both read and write heavy. Since the user would be sending messages and also viewing them.`

**Question**: `Out of the 3 parts of the CAP theorem, which one would you choose for your system?`

**Answer**: 
```High consistency and network partition tolerance. It will be a CP system.
This is because the user should not lose any messages and should be able to see the messages in the same order as they were sent.
```

---
## Sharding

**Question**: `Do you need to shard your database?`

**Answer**:
```
Yes, since the data is huge and we need to distribute it across multiple servers.
```

**Question**: `What would be the different candidate keys for sharding?`

**Answer**:
```
- UserId
- ConversationId
```

### Candidate key 1 - UserId

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- getRecentConversations(user_id)
    - Number of hops - 1 (since we can directly go to the user's data)
- getMessages(conversation_id, user_id, limit, offset)
    - Number of hops - 1 (since we can directly go to the user's data)
- sendMessage(conversation_id, sender_id, message)
    - Number of hops - 2 (since we need to go to the conversation data and then to the receiver's data)
```

### Candidate key 2

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- getRecentConversations(user_id)
    - Number of hops - N (since we need to go to all the machines to get the data)
- getMessages(conversation_id, user_id, limit, offset)
    - Number of hops - 1 (since we can directly go to the conversation data)
- sendMessage(conversation_id, sender_id, message)
    - Number of hops - 1 (since we can directly go to the conversation data)
```

**Final choice**: 
```
UserId. Two writes are not bad.
We will have to think of how to maintain consistency across the writes when the user is sending a message.
```

**Question**: `Do you require any other component to optimise your sharding strategy?`

**Answer**: 
```
You can think of using a secondary database to optimise the sharding when conversation ID is used as the sharding key.
However, it would increase the number of writes and also the complexity of the system.
```

---
## Design compliance

## Consistency
**Question** - `If you chose high consistency, how would you ensure that the system is consistent?`

**Answer** - 

Case 1 - Write to the sender shard first and then to the receiver shard

```
Flow -
- User sends a message
- Write the message to the sender's shard
    - If the write fails, the user will get an error
- Write the message to the receiver's shard
    - If the write fails, rollback the write to the sender's shard and return an error to the user
    - If the write is successful, return success to the user
```

Case 2 - Write to the sender shard and then to the receiver shard

```
Flow -
- User sends a message
- Write the message to the sender's shard
  - If the write fails, the user will get an error
- Write the message to the receiver's shard
  - If the write fails, retry the write. It will eventually succeed
  - If the write is successful, return success to the user
```

## Database

**Question** - `What kind of database would you choose for the messenger app?`

**Answer** - 
```
The system is both read and write heavy. We have to decompose the system to either read or write heavy.

To make it read heavy, you will have to absorb the writes. This generally works for systems where care about trends and it is okay for the system to loosely consistent.

To make it write heavy, you will have to absorb the reads. This generally works for systems where you need to be consistent and the user should not lose any data. To absorb the reads, you can use a cache. In this case, you also will have to think about a) how to maintain consistency across the cache and the database and b) how to handle the amount of incoming data.

A good write heavy database that can handle a heavy volume of data and also allows column based storage is HBase. It is a NoSQL database and can handle a huge amount of data. You can also use Cassandra. It is a distributed database and can handle a huge amount of data. It is also highly available and fault-tolerant.
```









