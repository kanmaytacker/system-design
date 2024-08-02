### Recap: NoSQL Internals - Write ahead logs (WAL), Memtables, and SSTables

Hello everyone! 👋 Here’s a summary of our discussion on the internals of NoSQL databases, focusing on Write Ahead Logs (WAL), Memtables, and SSTables:

🔍 **NoSQL Database Systems**
- NoSQL databases handle unstructured data with dynamic schemas, unlike structured SQL databases. This flexibility presents unique challenges and requires different data storage and retrieval strategies.

📝 **Key Concepts**
- **Write Ahead Log (WAL)**: This logging method ensures data integrity by recording changes before they're actually made to the database.
- **Memtable**: A high-performance, in-memory data structure where data is temporarily stored before being written to disk.
- **SSTable**: A disk-based data structure that stores data in a sorted sequence, which helps in efficient data retrieval.

📦 **Storage Challenges in NoSQL**
- Dynamic schemas and unstructured data make efficient data storage challenging. Traditional storage methods aren't effective due to varying data types and sizes.

🛠️ **Developed Solutions**
1. **WAL**: Provides data safety but increases storage as it records every change.
2. **Compaction**: Merges multiple entries of the same key in WAL to save space and maintain efficiency.
3. **Memtables and SSTables**: Use of in-memory structures coupled with sorted disk storage to balance read and write speeds efficiently.

📊 **Storage Engine Mechanics**
- Memtables serve current read/write requests with high speed, flushing to SSTables when full.
- SSTables store data in sorted blocks on disk, making read operations efficient with binary search facilitated by index tables.

🌟 **Pros and Cons**
- These mechanisms provide robust data integrity, high availability, and quick access speeds but can be complex to implement and require significant system resources to manage effectively.
