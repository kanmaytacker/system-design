# Elastic search

### 1. Create an Index
This is typically done via the Dev Tools in Kibana (Console).

```json
PUT /linkedin_posts
{
  "mappings": {
    "properties": {
      "author": {
        "type": "text"
      },
      "content": {
        "type": "text"
      },
      "date": {
        "type": "date"
      },
      "tags": {
        "type": "keyword"
      }
    }
  }
}
```

### 2. Index Some Documents
Add documents to the `linkedin_posts` index.

```json
POST /linkedin_posts/_doc/1
{
  "author": "John Doe",
  "content": "Excited to announce my new job at Tech Corp!",
  "date": "2024-08-05",
  "tags": ["announcement", "job"]
}

POST /linkedin_posts/_doc/2
{
  "author": "Jane Smith",
  "content": "Had a great time at the Tech Conference 2024!",
  "date": "2024-07-20",
  "tags": ["conference", "tech"]
}

POST /linkedin_posts/_doc/3
{
  "author": "Alice Johnson",
  "content": "Looking for talented software engineers to join our team.",
  "date": "2024-07-22",
  "tags": ["hiring", "jobs"]
}
```

### 3. Search for Documents

#### Search by Content
Search for posts containing the word "job".

```json
GET /linkedin_posts/_search
{
  "query": {
    "match": {
      "content": "job"
    }
  }
}
```

#### Search by Author
Search for posts by "Jane Smith".

```json
GET /linkedin_posts/_search
{
  "query": {
    "match": {
      "author": "Jane Smith"
    }
  }
}
```

#### Search by Tags
Search for posts with the tag "tech".

```json
GET /linkedin_posts/_search
{
  "query": {
    "term": {
      "tags": "tech"
    }
  }
}
```

### 4. Retrieve a Document by ID
Retrieve the document with ID 1.

```json
GET /linkedin_posts/_doc/1
```

### 5. Update a Document
Update the content of the document with ID 1.

```json
POST /linkedin_posts/_update/1
{
  "doc": {
    "content": "Excited to announce my new job at Tech Corp! Join me in this new journey."
  }
}
```

### 6. Delete a Document
Delete the document with ID 1.

```json
DELETE /linkedin_posts/_doc/1
```

### Summary in Kibana Console

- **Create Index**:
```json
PUT /linkedin_posts
{
  "mappings": {
    "properties": {
      "author": {
        "type": "text"
      },
      "content": {
        "type": "text"
      },
      "date": {
        "type": "date"
      },
      "tags": {
        "type": "keyword"
      }
    }
  }
}
```

- **Add Documents**:
```json
POST /linkedin_posts/_doc/1
{
  "author": "John Doe",
  "content": "Excited to announce my new job at Tech Corp!",
  "date": "2024-08-05",
  "tags": ["announcement", "job"]
}

POST /linkedin_posts/_doc/2
{
  "author": "Jane Smith",
  "content": "Had a great time at the Tech Conference 2024!",
  "date": "2024-07-20",
  "tags": ["conference", "tech"]
}

POST /linkedin_posts/_doc/3
{
  "author": "Alice Johnson",
  "content": "Looking for talented software engineers to join our team.",
  "date": "2024-07-22",
  "tags": ["hiring", "jobs"]
}
```

- **Search Documents**:
```json
GET /linkedin_posts/_search
{
  "query": {
    "match": {
      "content": "job"
    }
  }
}

GET /linkedin_posts/_search
{
  "query": {
    "match": {
      "author": "Jane Smith"
    }
  }
}

GET /linkedin_posts/_search
{
  "query": {
    "term": {
      "tags": "tech"
    }
  }
}
```

- **Retrieve by ID**:
```json
GET /linkedin_posts/_doc/1
```

- **Update Document**:
```json
POST /linkedin_posts/_update/1
{
  "doc": {
    "content": "Excited to announce my new job at Tech Corp! Join me in this new journey."
  }
}
```

- **Delete Document**:
```json
DELETE /linkedin_posts/_doc/1
```
---

## Advanced Elasticsearch Queries

### 1. **Full-Text Search with Multiple Fields**

Search for posts that mention "engineer" in either the content or the tags.

```json
GET /linkedin_posts/_search
{
  "query": {
    "multi_match": {
      "query": "engineer",
      "fields": ["content", "tags"]
    }
  }
}
```

### 2. **Phrase Search**

Search for posts that contain the exact phrase "software engineer".

```json
GET /linkedin_posts/_search
{
  "query": {
    "match_phrase": {
      "content": "software engineer"
    }
  }
}
```

### 3. **Boolean Query**

Search for posts that contain "job" but not "tech".

```json
GET /linkedin_posts/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "content": "job"
        }
      },
      "must_not": {
        "match": {
          "content": "tech"
        }
      }
    }
  }
}
```

### 4. **Filter by Date Range**

Search for posts made between July 1, 2024, and July 31, 2024.

```json
GET /linkedin_posts/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "2024-07-01",
        "lte": "2024-07-31"
      }
    }
  }
}
```

### 5. **Aggregation: Count of Posts per Tag**

Get the count of posts for each tag.

```json
GET /linkedin_posts/_search
{
  "size": 0,
  "aggs": {
    "tags_count": {
      "terms": {
        "field": "tags.keyword"
      }
    }
  }
}
```

### 6. **Aggregation: Monthly Activity**

Get the count of posts per month.

```json
GET /linkedin_posts/_search
{
  "size": 0,
  "aggs": {
    "monthly_activity": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "month"
      }
    }
  }
}
```

### 7. **Highlighting Search Terms**

Highlight the term "job" in the search results.

```json
GET /linkedin_posts/_search
{
  "query": {
    "match": {
      "content": "job"
    }
  },
  "highlight": {
    "fields": {
      "content": {}
    }
  }
}
```

### 8. **Combining Multiple Criteria**

Search for posts by "John Doe" that mention "engineer" and were posted in July 2024.

```json
GET /linkedin_posts/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "author": "John Doe"
          }
        },
        {
          "match": {
            "content": "engineer"
          }
        },
        {
          "range": {
            "date": {
              "gte": "2024-07-01",
              "lte": "2024-07-31"
            }
          }
        }
      ]
    }
  }
}
```

### 9. **Fuzzy Search**

Search for posts with terms similar to "enginer".

```json
GET /linkedin_posts/_search
{
  "query": {
    "fuzzy": {
      "content": {
        "value": "enginer",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

### 10. **Nested Queries for Nested Documents**

If you have nested objects in your documents, you can use nested queries. Assuming `comments` is a nested field:

```json
GET /linkedin_posts/_search
{
  "query": {
    "nested": {
      "path": "comments",
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "comments.text": "great post"
              }
            },
            {
              "match": {
                "comments.user": "Jane Smith"
              }
            }
          ]
        }
      }
    }
  }
}
```

### 11. **Scripted Fields**

Use a script to create a custom score based on the length of the content.

```json
GET /linkedin_posts/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": "doc['content'].value.length()"
        }
      }
    }
  }
}
```
