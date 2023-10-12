# NoSQL Internals - Write ahead logs (WAL), Memtables and SSTables

- [NoSQL Internals - Write ahead logs (WAL), Memtables and SSTables](#nosql-internals---write-ahead-logs-wal-memtables-and-sstables)
  - [Key Terms](#key-terms)
    - [NoSQL Database](#nosql-database)
    - [Write Ahead Log (WAL)](#write-ahead-log-wal)
    - [Memtable](#memtable)
    - [SSTable](#sstable)
  - [Motivation](#motivation)
  - [Problem Statement](#problem-statement)
  - [Solution 1 - Store the data in a file](#solution-1---store-the-data-in-a-file)
  - [Solution 2 - Write Ahead Log (WAL)](#solution-2---write-ahead-log-wal)
  - [Solution 3 - WAL with an index table](#solution-3---wal-with-an-index-table)
  - [Solution 4 - How to handle the duplicate data? Compaction](#solution-4---how-to-handle-the-duplicate-data-compaction)
  - [Solution 5 - Memtables and SSTables](#solution-5---memtables-and-sstables)
  - [Further questions:](#further-questions)
    - [Additional Resources](#additional-resources)

## Key Terms

### NoSQL Database

> A NoSQL database is a non-relational database that provides a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases. They store data in an unstructured format, unlike relational databases, and are designed to handle large data sets that can be distributed across multiple servers efficiently.

### Write Ahead Log (WAL)

> A write-ahead log (WAL) is a standard method for ensuring data integrity. A WAL file is a file that contains a record of changes made to data. The changes are first recorded in the log file before the actual modifications are made to the database. This ensures that no modifications are lost even if the system fails.

### Memtable

> A memtable is a temporary, in-memory data structure used by some key-value stores to achieve high write performance. It is a write-back cache of data rows that have been updated on disk.


### SSTable

> A sorted string table (SSTable) is a file that contains a sequence of key-value pairs, which are sorted by key. SSTables are the main storage format used by Apache Cassandra.

## Motivation

One of the major differences between SQL and NoSQL databases is the type of data that is stored in them. SQL databases store structured data while NoSQL databases store unstructured data. This means that SQL databases have a fixed schema while NoSQL databases have a dynamic schema.

While, this is great advantage of NoSQL databases, it also means that the data storage is not trivial. In order to store unstructured data, NoSQL databases need to have a way to store the data in a way that it can be retrieved efficiently. Let us take an example to understand this better.

Let us say we have a list of simple rows as below:

| id  | name            |
| --- | --------------- |
| 1   | Tantia Tope     |
| 2   | Sherlock Holmes |
| 3   | Moriarty        |

Now a SQL database follows a schema and hence we always know that the both these columns will be required for each row. Also, the columns will be of a fixed type such as `int` or `varchar`. Both these factors help us in storing the data in a very efficient manner. Since the number of bytes required to store each row is fixed, we can easily calculate the offset of each row and hence retrieve it efficiently. 
**This is not the case with NoSQL databases.**

Since the schema is dynamic, we cannot assume that each row will have the same number of columns. Also, since the columns can be of different types, we cannot assume that each column will take the same number of bytes. This makes it very difficult to store the data in a way that it can be retrieved efficiently. Updating an item in-place will either require us to shift the entire data or leave gaps in the data. The former is very expensive, while the latter leaves our data in a very fragmented state. So, a new approach is required to store the data in a way that it can be retrieved efficiently.

## Problem Statement

To understand the way NoSQL databases store data, we will approach it as a problem statement. We are going create the storage engine for a key-value datastore like Redis. The datastore will be a simple key-value store with the following operations:
1. `get(key)`: Returns the value for the given key.
2. `set(key, value)`: Sets the value for the given key. If the key already exists, the value is overwritten.

*The goal is to store the data in a way that it can be retrieved efficiently.*

## Solution 1 - Store the data in a file

The simplest way to store the data is to store it in a file. Let us take an example for the following key value pairs:

```json
{
  "1": "Tantia Tope",
  "2": "Sherlock Holmes",
  "3": "Moriarty"
}
```

For the above key value pairs, we can construct a file which stores the key and value as a row in the file. The file will look like this:

| key | value           |
| --- | --------------- |
| 1   | Tantia Tope     |
| 2   | Sherlock Holmes |
| 3   | Moriarty        |

This data will be stored in the disk and reading and writing will require operations on the same file. Let us see how the `get` and `set` operations will work.

1. `get(key)`: To get the value for a given key, we will have to read the entire file and find the row with the given key. This is a very expensive operation and will take a lot of time i.e. `O(n)` time.
2. `set(key, value)`: To set the value for a given key, we will have to read the entire file and find the row with the given key. Once we find the row, we will have to update the value in the row. If the key is not found, we will have to append a new row to the file. This will also take a lot of time i.e. `O(n)` time.

**While a simple solution, this is extremely inefficient. Can we do better?**

## Solution 2 - Write Ahead Log (WAL)

Write ahead logging is a technique used in databases to ensure that the data is written to the disk before it is written to the database. This ensures that the data is not lost even if the system fails. Let's say the current state of the database is as follows:

| key | value           |
| --- | --------------- |
| 1   | Tantia Tope     |
| 2   | Sherlock Holmes |
| 3   | Moriarty        |

Now, let's say we want to update the value for the key `2` to `John Watson`. In a WAL file each row is immutable. So, we cannot update the value for the key `2`. Instead, we will have to append a new row to the file. The file will now look like this:

| key | value           |
| --- | --------------- |
| 1   | Tantia Tope     |
| 2   | Sherlock Holmes |
| 3   | Moriarty        |
| 2   | John Watson     |

Let's compare the operations of `get` and `set` with the previous solution.

1. `update(key, value)`: To update the value for a given key or add a new key value pair, we will have to append a new row to the file. We no longer have to read the entire file to find the row with the given key. This is a much more efficient operation and will take `O(1)` time.
2. `get(key)`: Since a file now has multiple rows with the same key, the read operation can be tricky. We will read the file from the end and find the first row with the given key. However, the worst case time complexity will still be `O(n)`.

**While this is a much better solution, it still has some problems.**:
1. `Wastage of space`: Since we are appending a new row for each update, we are wasting a lot of space. This is because we are storing the same key multiple times.
2. `Read operation is still expensive`: While the write operation is now efficient, the read operation is still expensive. This is because we have to read the entire file to find the row with the given key.

Can you think of a way to improve this solution?

## Solution 3 - WAL with an index table

To make the reads faster we can take a page out of the SQL databases. SQL databases use indexes to make the reads faster. An index is a data structure that stores the key and the offset of the row in the file. We can use a similar approach to make the reads faster.
Let's say we have the following file:

| Address | ID  | Name            |
| ------- | --- | --------------- |
| 3000    | 1   | Tantia Tope     |
| 3001    | 2   | Sherlock Holmes |
| 3000    | 3   | Moriarty        |

We can create an index table that stores the key and the offset of the row or the address of the row in the file. The index table will look like this:

| key | address |
| --- | ------- |
| 1   | 3000    |
| 2   | 3001    |
| 3   | 3002    |

Let us see how the `get` and `set` operations will work with this approach:
1. `get(key)`: To get the value for a given key, we will have to read the index table and find the address of the row with the given key. Once we have the address, we can read the row from the file. This is a much more efficient operation and will take `O(1)` time.
2. `update(key, value)`: To update the value for a given key or add a new key value pair, we will have to append a new row to the file and update the index table. We no longer have to read the entire file to find the row with the given key. This is a much more efficient operation and will take `O(1)` time.

**Can you identify the problems with this approach?**

1. `Memory utilisation` - While the read and write operations are now efficient, we have introduced a new problem. The index table is stored in the memory and hence it is limited by the size of the memory. This means that we can only store a limited number of key value pairs in the database. This is a major problem and needs to be solved. For example, if we have 10 million rows in the database, we will need to store 10 million rows. This will require a lot of memory.
2. `Duplicate data` - We are still storing the same key multiple times in the file. This is a waste of space and needs to be solved.

## Solution 4 - How to handle the duplicate data? Compaction

One of the problems we are facing with immutable rows is that we are storing the same key multiple times. This is a waste of space and specially in write-heavy applications. To solve this problem, we can use a technique called compaction. Compaction is a process of merging multiple rows with the same key into a single row. This can be done as a background process and will not affect the read and write operations. Let us see how the compaction process will work.

1. `Periodic execution` - On a fixed interval, we will run a compaction process. This will execute as a background process and will not affect the read and write operations.
2. `Read the file` - The compaction process will read the file in chunks of let's say 1000 rows. This is to ensure that the entire file is not read at once.
3. `Deduplicate the rows` - The compaction process will identify if a key does not have same address as in the index table. This means that the row has been updated.
4. `Create a new file and index table` - If a key has the same address in the WAL file as the index table, it means that the row has not been updated. In this case, we will create a new file and index table and copy the rows from the old file to the new file. We will also update the index table with the new address of the row in the new file.

This approach will ensure that the duplicate data is removed from the file and the index table. While it is an expensive process, it can run at fixed intervals to reduce the load on the system. However, we still have not fixed our read efficiency problem. Let us see how we can fix that.

## Solution 5 - Memtables and SSTables

We have seen that the index table is stored in the memory and hence it is limited by the size of the memory. This means that we can only store a limited number of key value pairs in the database. This is a major problem and needs to be solved. For example, if we have 10 million rows in the database, we will need to store 10 million rows. This will require a lot of memory.

To solve this problem, we can use a technique called memtables. A memtable is a temporary, in-memory data structure used by some key-value stores to achieve high read and write performance. It is a write-back cache of data rows that have been updated on disk. Let us see how this will work.

We will use the same technique as the background process to chunk the file into smaller portions. The latest chunk will be stored in the memory and is known as a memtable. The memtable will be stored in the memory and will be used for all the read and write operations. Once the memtable is full, it will be flushed to the disk and a new memtable will be created. This will ensure that the data is stored in the disk and the memory is freed up for new data. The memtable can be stored as treemap in memory which has sorted keys. This will ensure that the read operations are efficient.

Let us compare our operations now:

1. `get(key)`: To get the value for a given key, we will have to read the memtable and find the row with the given key. If the row is not found, we will have to read to go the disk.
2. `update(key, value)`: To update the value for a given key or add a new key value pair, we will have to overwrite the value in the memtable. Once the memtable is full, it will be flushed to the disk. Writing an item to the memtable is an `O(logN)` operation.

The write operation is efficient since we are writing to the memory. The read operation is efficient as long as the data is in the memtable. Once the memtable is full, the read operation will be expensive. To solve this problem, we can use a technique called SSTables. A sorted string table (SSTable) is a file that contains a sequence of key-value pairs, which are sorted by key. SSTables are the main storage format used by Apache Cassandra. Let us see how this will work.

As mentioned above, the files are stored in the disk in smaller partitions. To make the reads efficient, we will also store the data in the disk in sorted order. This will help us in seeking to a particular row in the file. This approach of storing the data in chunks in a sorted order is known as `SSTables`. 

Let use see the current state of our read operation:

1. `Key found` - If we get a key, first check the key in the memtable. If the key is found, we can return the value. This will be an `O(logN)` operation.
2. `Key not found` - If the key is not found in the memtable, we will have to read the SSTables. We will read the SSTables in the reverse order and find the first row with the given key. This will be an `O(n)` operation since it possible that the key is not found in the SSTables.

How do we optimise the read operation? This is where use the fact that our keys are sorted. We should ideally be able to run a binary search on the SSTables to find the row with the given key. However, since the SSTables are stored in the disk, we cannot run a binary search on them. This is because the size of the rows is not fixed and hence we cannot calculate the offset of each row.

To solve this problem, we will create an index table for the SSTables. The index table will store the first key in the chunk and the start address of the chunk. Now, we can run a binary search on the index table to find the chunk with the given key. Once we find the chunk, we can read the chunk and find the row with the given key. This will be an `O(logN)` operation and then reading the chunk from the disk. Let us have a look at all the different storage components we have now.

Let us say we have a bunch of rows that we want to store;

| key | value |
| --- | ----- |
| 1   | A     |
| 2   | B     |
| 3   | C     |
| 4   | D     |
| 5   | E     |

We will first divide the rows into different `SSTables`

`SSTable 1`
| ADDRESS | KEY | VALUE |
| ------- | --- | ----- |
| 1000    | 1   | A     |
| 1001    | 2   | B     |

`SSTable 2`
| ADDRESS | KEY | VALUE |
| ------- | --- | ----- |
| 2000    | 3   | C     |
| 2001    | 4   | D     |


Let's assume the last value is stored in memory as a memtable. This would look like

`Memtable`
| KEY | VALUE |
| --- | ----- |
| 5   | E     |

For the index table, we will store the first key and the address of the chunk. This will look like:

`Index Table`
| KEY | ADDRESS |
| --- | ------- |
| 1   | 1000    |
| 3   | 2000    |

Now, let us see how the read operations will work:

1. `Memtable` - Check if the read key is present in the memtable. If yes, return the value.
2. `Index table` - If the key is not present in the memtable, check the index table. If the key is present in the index table, find the chunk with the given key.
3. `SSTable` - Get the chunk from the SSTable and find the row with the given key.

Let us take the example of `get(4)` to understand this better:
1. `Check the memtable`. The key is not present in the memtable.
2. `Check the index table`. The key is present in the index table. The chunk with the key is `SSTable 2`.
3. `Read the chunk from the SSTable`. The chunk is read from the SSTable and the row with the given key is found.

## Further questions:
- **What happens if the machine storing this entry reboots / restarts? Everything in the memTable will be lost since it was RAM only. How do we recover?**
  - WAL comes to our rescue here. Before this machine resumes, it has to replay logs made after the last disk flush to reconstruct the right state of memTable. Since all operations are done in memory, you can replay logs really fast (slowest step being reading WAL logs from the disk).

- **How does delete a key work?**
  - What if delete is also another (key, value) entry where we assign a unique value denoting a tombstone. If the latest value you read is a tombstone, you return “key does not exist”.

- **As you would have noticed, read for a key not found is very expensive. You look it up in every sorted set, which means you scan multiple 64Kb blocks before figuring out the key does not exist. That is a lot of work for no return (literally). How do we optimize that?**
- Bloom Filter. A filter which works in the following way:
Function:
  - doesKeyExist(key) :
    - return false -> Key definitely does not exist.
    - return true -> Key may or may not exist.

So, if the function returns false, you can directly return “key does not exist” without having to scan SSTables. The more accurate your bloom function, the more optimization you get.

Also, another prerequisite is that the bloom filter has to be space efficient. It should fit in memory and utilize as little space there as possible.
https://llimllib.github.io/bloomfilter-tutorial/ has a simple, interactive explanation of BloomFilter (also explained in class).

### Additional Resources
- [Bloom Filters](https://llimllib.github.io/bloomfilter-tutorial/)
- [LSM trees](https://dev.to/creativcoder/what-is-a-lsm-tree-3d75)
- [NoSQL Databases](https://medium.com/@qiaojialinwolf/lsm-tree-the-underlying-design-of-nosql-database-cf30218e82f3)