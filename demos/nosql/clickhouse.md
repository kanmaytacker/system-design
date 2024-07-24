# Clickhouse commands and queries

Connect to the ClickHouse server:

```bash
docker exec -it clickhouse-server clickhouse-client
```

### Setting Up the Bookmarks Schema in ClickHouse

#### 1. **Create the Bookmarks Table**

```sql
CREATE TABLE bookmarks (
    id UUID,
    url String,
    title String,
    description String,
    tags Array(String),
    createdOn Date,
    userID UUID
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(createdOn)
ORDER BY (createdOn, id);
```

!!! note This table uses the `MergeTree` engine, which is optimal for read-heavy analytical workloads. The data is partitioned by month (`createdOn`) and ordered primarily by `createdOn` and secondarily by `id` for efficient querying.

### Example Queries


#### 2. **Inserting Data**

```sql
INSERT INTO bookmarks (id, url, title, description, tags, createdOn, userID) VALUES
(generateUUIDv4(), 'https://www.example.com', 'Example Website', 'This is an example website.', ['Education', 'Technology'], '2024-07-24', generateUUIDv4()),
(generateUUIDv4(), 'https://www.news.com', 'News Website', 'This is a news website.', ['News', 'Updates'], '2024-07-24', generateUUIDv4()),
(generateUUIDv4(), 'https://www.opensource.org', 'Open Source', 'Explore open source projects.', ['Coding', 'Technology'], '2024-07-24', generateUUIDv4());
```

#### 3. **Select All Bookmarks**

```sql
SELECT *
FROM bookmarks;
```

#### 4. **Aggregate Query - Count Bookmarks by Tag**


```sql
SELECT tag, count() AS total_bookmarks
FROM bookmarks
ARRAY JOIN tags AS tag
GROUP BY tag
ORDER BY total_bookmarks DESC;
```

#### 5. **Filter Bookmarks by Tag**

```sql
SELECT url, title, description
FROM bookmarks
WHERE has(tags, 'Technology');
```

#### 6. **Date Range Queries**

Find bookmarks created within a specific date range:

```sql
SELECT *
FROM bookmarks
WHERE createdOn BETWEEN '2024-07-01' AND '2024-07-31';
```

#### 7. **Complex Query - Most Popular Tags per Month**

```sql
SELECT toYYYYMM(createdOn) AS month, tag, count() AS count
FROM bookmarks
ARRAY JOIN tags AS tag
GROUP BY month, tag
ORDER BY month, count DESC;
```