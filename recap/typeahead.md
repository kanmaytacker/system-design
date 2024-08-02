📚 Class Recap: Typeahead search case study

Hello everyone! 👋 Here is a summary of what we discussed in today's session:

🔍 *Typeahead search*
- Typeahead search, also known as autocomplete or autosuggest, is a feature that suggests search queries or results as users type in a search box.
- It helps users find relevant information quickly, reduces typing effort, and improves the search experience.
- Typeahead search is commonly used in search engines, e-commerce platforms, social media sites, and other applications with search functionality.

📝 *Requirements*
- The typeahead search should return 5 suggestions based on the user's input.
- The suggestions should be sorted popularity (e.g., frequency of search).
- The search should be triggered after the user types at least 3 characters.

📦 *Back-of-the-envelope calculations*
- Google receives 10 billion search queries in a day and each query results in 6 typeahead calls on average. This means Google handles 60 billion typeahead requests per day.
- Not every request will result in a write operation, but let's assume 10% of the requests are new and need to be stored in the database. This results in 1 billion write operations per day or 36 billion write operations per year.
- The average size of a row in the database is 40 bytes (search query + frequency). This results in 40 GB of new data per day or 14.6 TB per year.

📊 *System design considerations*
- The write operation is updating the frequency of search queries, while read is fetching the top 5 suggestions based on the user input.
- From the assumptions above, for every 1 write operation, there are 6 read operations.
- There is not a significant difference between read and write operations, so the system can be considered balanced in terms of read and write load. The order of magnitude of read and write operations is the same.
- The system should also prioritise availability over consistency, as users expect real-time suggestions when typing in the search box. The system will be eventually consistent.
- By PACELC theorem, the system should be designed to be available and partition-tolerant, while allowing for eventual consistency and low latency.

<!-- Brute force -->
🔨 *Brute force approach*
- For generating suggestions, we can use a brute force approach where we scan the entire database to find matching search queries based on the user input. The query would look like `SELECT query FROM search_queries WHERE query LIKE 'input%' ORDER BY frequency DESC LIMIT 5`.
- This approach is simple and works well for small datasets, but it can be slow and inefficient for large datasets as it requires scanning the entire database for each request. The LIKE operator can also be slow for wildcard searches.

🗄️ *Using a Key-Value Store*
- To improve the performance of the system, we can use a key-value store like Redis to store search queries and their frequencies (*Frequency*). Redis allows for fast read and write operations, making it suitable for real-time suggestions.
- To generate suggestions, we can also store all the possible set of prefixes of the search queries and their corresponding suggestions in Redis (*Top5Suggestions*). For example, the key would be `sher` and the value would be `[sherlock, sherlock holmes, sherlock tv series, sherlock cast, sherlock holmes books]`.
  
🔧 *Operations on Redis*
- `Update frequency`: When a user searches for a query, we increment the frequency of that query in *Frequency*. If the query does not exist, we add it with a frequency of 1. The data can be propagated to the database periodically for persistence as a write-back cache.
- `Update suggestions`: The frequency update would also need to update the suggestions in *Top5Suggestions*. However, it doesn't need to be done in real-time and can be done periodically to reduce the write load and in line with our eventual consistency model.
- `Generate suggestions`: To generate suggestions, we can fetch the top 5 suggestions from *Top5Suggestions* based on the user input. For example, if the user types `sher`, we fetch the suggestions for the key `sher` from Redis.

<!-- Advantages and disadvantages -->
🌟 *Pros and cons of the Redis approach*

- Redis is an in-memory data store, which allows for fast read and write operations, making it suitable for real-time suggestions.
- The approach of storing prefixes and suggestions in Redis allows for efficient retrieval of suggestions based on user input.
- However, Redis is an in-memory store, which means it has limited storage capacity compared to disk-based databases. This can be a limitation when dealing with large datasets.
- Redis can be scaled horizontally by sharding data across multiple instances based on a consistent hashing algorithm, with the sharding key being the search query prefix.
- The space complexity of storing all possible prefixes and suggestions in Redis can be high, especially for long search queries. This can be mitigated by using techniques like prefix compression or storing only the most popular prefixes.

🌳 *Trie approach*
- Another approach to implement typeahead search is by using a trie data structure. A trie is a tree-like data structure that stores a dynamic set of strings, making it efficient for prefix searches.
- Each node in the trie represents a character, and the edges represent the next character in the string. The node will contain the character, a list of suggestions and frequency of the path to that node.
- To generate suggestions, we traverse the trie based on the user input and return the suggestions stored at the node corresponding to the input prefix.
- To update the frequency of search queries, we traverse the trie to find the node corresponding to the query and increment the frequency. The suggestions can be updated periodically based on the updated frequencies.


🌟 *Pros of the Trie approach*
- The trie can be stored in memory for fast read and write operations, and can be persisted to disk for durability.
- Tries are efficient for prefix searches and can provide fast suggestions based on user input. The worst-case time complexity for searching in a trie is O(m), where m is the length of the search query.
- The update operations in a trie are also efficient, with a time complexity of O(m) for inserting or updating a search query.
- The space complexity, when compared to storing all prefixes in Redis, can be more efficient as tries store common prefixes only once.

🌳 *Cons of the Trie approach*
- However, the space complexity of a trie can be high for large datasets with long search queries, especially if the trie is not compressed or optimised.
- Also, storing the trie in memory can be a limitation for large datasets, as it may require a significant amount of memory.
- This can be mitigated by using techniques like prefix compression, storing only the most popular prefixes, or sharding the trie across multiple instances.

📊 *Reads vs writes*
- The system is both read and write-heavy, with reads being more frequent than writes. This is sub-optimal as the reads and writes will compete for resources.
- `Buffering writes`: To handle the write-heavy nature of the system, we can buffer the write operations in memory and periodically flush them to the database. This can reduce the load on the database and improve write performance.
- `Sampling writes`: We can also sample the write operations and only update the frequency for once every n requests. This can reduce the number of write operations.
- `Buffering vs sampling`: The difference between buffering and sampling is that buffering accumulates write operations in memory and flushes them periodically, while sampling reduces the frequency of write operations by updating the frequency less frequently.

📚 *Assignment*
For today's assignment, I want you to think about how you can incorporate a recency factor into the typeahead search system. Currently, the suggestions are based on popularity (frequency of search).

How can you also consider the recency of search queries and provide more weight to recent searches in the suggestions? Think about how you can update the suggestions based on both popularity and recency. Can you disadvantage the popularity of a search query with time?

Feel free to share your thoughts and ideas in the group! 
See you in the next class! 🚀