# Elasticsearch

## Setup

To start Elasticsearch with Docker Compose, use the following command:

```bash
docker-compose up -d
```

To verify that the Elasticsearch container is running, you can use the following command:

```bash
docker-compose ps
```

You can also call the Elasticsearch REST API to check if it's running with curl:

```bash
curl -X GET "localhost:9200"
```

---

### Create an Index

To create an index called `linkedin_posts`, use the following `curl` command:

```bash
curl -X PUT "localhost:9200/linkedin_posts" -H 'Content-Type: application/json' -d'
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
'
```

### Index the documents

You can add documents to the `linkedin_posts` index with the following commands:

```bash
curl -X POST "localhost:9200/linkedin_posts/_doc/1" -H 'Content-Type: application/json' -d'
{
  "author": "John Doe",
  "content": "Excited to announce my new job at Tech Corp!",
  "date": "2024-08-05",
  "tags": ["announcement", "job"]
}
'

curl -X POST "localhost:9200/linkedin_posts/_doc/2" -H 'Content-Type: application/json' -d'
{
  "author": "Jane Smith",
  "content": "Had a great time at the Tech Conference 2024!",
  "date": "2024-07-20",
  "tags": ["conference", "tech"]
}
'

curl -X POST "localhost:9200/linkedin_posts/_doc/3" -H 'Content-Type: application/json' -d'
{
  "author": "Alice Johnson",
  "content": "Looking for talented software engineers to join our team.",
  "date": "2024-07-22",
  "tags": ["hiring", "jobs"]
}
'
```

or in one go:

```bash
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' -d'
{ "index": { "_index": "linkedin_posts", "_id": "1" }}
{ "author": "John Doe", "content": "Excited to announce my new job at Tech Corp!", "date": "2024-08-05", "tags": ["announcement", "job"] }
{ "index": { "_index": "linkedin_posts", "_id": "2" }}
{ "author": "Jane Smith", "content": "Had a great time at the Tech Conference 2024!", "date": "2024-07-20", "tags": ["conference", "tech"] }
{ "index": { "_index": "linkedin_posts", "_id": "3" }}
{ "author": "Alice Johnson", "content": "Looking for talented software engineers to join our team.", "date": "2024-07-22", "tags": ["hiring", "jobs"] }
'
```

### Queries

You can search for documents containing the word `job` in the `content` field:

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "content": "job"
    }
  }
}
'
```

The following command searches for posts by `Jane Smith`:

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "author": "Jane Smith"
    }
  }
}
'
```

You can even search for text in collections (arrays) like `tags`:

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "tags": "tech"
    }
  }
}
'
```

To retrieve the document with ID 1, use the following:

```bash
curl -X GET "localhost:9200/linkedin_posts/_doc/1"
```

To update the content of the document with ID 1:

```bash
curl -X POST "localhost:9200/linkedin_posts/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "content": "Excited to announce my new job at Tech Corp! Join me in this new journey."
  }
}
'
```

You can delete the document with ID 1 using the following command:

```bash
curl -X DELETE "localhost:9200/linkedin_posts/_doc/1"
```

---

**Task**: Search for posts that mention `job` in either the content or the tags.

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "multi_match": {
      "query": "engineer",
      "fields": ["content", "tags"]
    }
  }
}
'
```

**Task**: Search for posts that contain the exact phrase `software engineers`

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_phrase": {
      "content": "software engineer"
    }
  }
}'
```

**Task**: Search for posts that contain "job" but not "tech".

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
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
'
```

**Task**: Search for posts made between July 1, 2024, and July 31, 2024.

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "date": {
        "gte": "2024-07-01",
        "lte": "2024-07-31"
      }
    }
  }
}'
```

**Task**: Get the count of posts for each tag.

```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "tags_count": {
      "terms": {
        "field": "tags.keyword"
      }
    }
  }
}'
```

**Task**: Search for posts that contain `engineers` but not `tech`.
```bash
curl -X GET "localhost:9200/linkedin_posts/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "content": "engineers"
        }
      },
      "must_not": {
        "match": {
          "content": "tech"
        }
      }
    }
  }
}'
```
