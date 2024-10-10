# Redis commands

!!! info
    You should have the Redis server already running through Docker Compose. Verify it by running either:
      - `docker-compose ps`
      - `docker exec -it redisjson redis-cli ping`


## Connect to Redis

To connect to the Redis server, run the following command:

```bash
docker exec -it redisjson redis-cli
```

## Basic Redis Commands

#### 1. **Strings**
- **Set a value:**
  ```bash
  SET key value
  ```
- **Get a value:**
  ```bash
  GET key
  ```
- **Set a value with an expiration time (in seconds):**
  ```bash
  SETEX key 10 value 
  ```
  You can also use `SET key value EX 10` to set the expiration time.

#### 2. **Hashes**
- **Set multiple fields in a hash:**
  ```bash
  HMSET key field1 value1 field2 value2
  ```
- **Get all fields and values from a hash:**
  ```bash
  HGETALL key
  ```
- **Get a specific field from a hash:**
  ```bash
  HGET key field1
  ```

#### 3. **Lists**
- **Push elements to the left of a list:**
  ```bash
  LPUSH mylist value1 value2
  ```
- **Retrieve a range of elements from a list:**
  ```bash
  LRANGE mylist 0 -1  # Returns all elements
  ```

#### 4. **Sets**
- **Add elements to a set:**
  ```bash
  SADD myset value1 value2
  ```
- **Get all elements of a set:**
  ```bash
  SMEMBERS myset
  ```

#### 5. **Sorted Sets**
- **Add elements with scores:**
  ```bash
  ZADD mysortedset 1 "one" 2 "two"
  ```
- **Get elements sorted by score:**
  ```bash
  ZRANGE mysortedset 0 -1 WITHSCORES
  ```

## Bookmarks

### **1. Choose a Key Schema**
Decide on a key naming convention. For bookmarks, you might use something like `bookmark:{id}` where `{id}` is a unique identifier for each bookmark. This helps in organizing and accessing bookmark data efficiently.

### **2. Use a Redis Hash to Store Bookmark Details**
Redis hashes are ideal for storing objects with multiple fields. You can use the `HMSET` command (or `HSET` in newer Redis versions as `HMSET` is deprecated) to store a bookmark. For example:

```bash
HSET bookmark:101 url "https://www.example.com" title "Example Website" description "This is an example website."
```

Here, `bookmark:101` is the key for a hash where `url`, `title`, and `description` are fields storing information about the bookmark.

#### **3. Retrieving a Bookmark**
To get all the details of the bookmark back, use `HGETALL`:

```bash
HGETALL bookmark:101
```

This command will return all fields and values of the hash stored at `bookmark:101`, such as:

```
1) "url"
2) "https://www.example.com"
3) "title"
4) "Example Website"
5) "description"
6) "This is an example website."
```

#### **4. Updating a Bookmark**
If you need to update a specific field of a bookmark, you can use `HSET` again:

```bash
HSET bookmark:101 description "Updated description of the example website."
```

This command will update the `description` field of the hash for `bookmark:101`.

#### **5. Deleting a Bookmark**
To delete an entire bookmark:

```bash
DEL bookmark:101
```

This command removes the entire hash identified by `bookmark:101`.

### Advanced Use: Adding Tags to a Bookmark

If you want to associate tags with bookmarks and be able to query bookmarks by tags, you might use Redis sets alongside hashes:

#### **1. Store Bookmark**
As above, store the bookmark details in a hash.

#### **2. Associate Tags with Bookmark Using Sets**
For each tag, you could create a set that stores the IDs of bookmarks associated with that tag:

```bash
SADD tag:Education bookmark:101
SADD tag:Technology bookmark:101
```

#### **3. Find Bookmarks by Tag**
To find all bookmarks with a given tag, like "Education":

```bash
SMEMBERS tag:Education
```

This command will return all bookmark IDs associated with the "Education" tag.

### Using RedisJSON to Store Bookmarks


#### **1. Store a Bookmark as a JSON**

You can use the `JSON.SET` command to store an entire JSON object:

```bash
JSON.SET bookmark:101 $ '{"url": "https://www.example.com", "title": "Example Website", "description": "This is an example website.", "tags": ["Education", "Technology"]}'
```

This command sets a JSON object for the key `bookmark:101`. The `$` signifies that you're setting the entire document.

#### **2. Retrieve the Entire Bookmark**

To retrieve the entire JSON object:

```bash
JSON.GET bookmark:101
```

This will return the full JSON document stored under the key `bookmark:101`.

#### **3. Retrieve Specific Fields**

If you only need specific fields from the JSON document, such as the `title`:

```bash
JSON.GET bookmark:101 $.title
```

This queries the JSON object for just the `title` field.

#### **4. Update Part of the Bookmark**

You can update just part of the JSON document without replacing the entire thing:

```bash
JSON.SET bookmark:101 $.description "Updated description of the example website."
```

This updates only the `description` field of the JSON object.

#### **5. Add a New Field**

To add a new field to the JSON object, for example, adding a `dateAdded` field:

```bash
JSON.SET bookmark:101 $.dateAdded "2024-07-24T12:00:00Z"
```