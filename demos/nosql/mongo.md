# Mongo queries

## User

### Insert the data

```json
[
  { "username": "tantia.tope", "email": "tantia.top@example.com" },
  { "username": "sherlock.holmes", "email": "sherlock.holmes@example.com" },
  { "username": "bruce.wayne", "email": "bruce.wayne@example.com" }
]
```

### Queries

- Get all users - `{}`
- Get the user with username `tantia.tope` - `{ "username": "tantia.tope" }`
- Get only the username of all users - `{ "username": 1, "_id": 0 }` (Projection)

## Bookmarks

### Insert the data

```json
[
  {
    "userID": {"$oid": "66a049b56be1d50137015edf"}, // Replace with the ID in your database
    "url": "https://www.example.com",
    "title": "Example Website",
    "description": "This is an example website.",
    "createdOn": {"$date": "2024-07-24T12:00:00Z"},
    "tags": ["Education", "Technology"]
  },
  {
    "userID": {"$oid": "66a049b56be1d50137015ee0"}, // Replace with the ID in your database
    "url": "https://www.news.com",
    "title": "News Website",
    "description": "This is a news website.",
    "createdOn": {"$date": "2024-07-24T13:00:00Z"},
    "tags": ["News", "Technology"]
  },
  {
    "userID": {"$oid": "66a049b56be1d50137015ee1"}, // Replace with the ID in your database
    "url": "https://www.opensource.org",
    "title": "Open Source",
    "description": "This is an open source community website.",
    "createdOn": {"$date": "2024-07-24T14:00:00Z"},
    "tags": ["Open Source"]
  }
]

```

### Queries

- Get all bookmarks - `{}`
- Get the bookmark with title `Example Website` - `{ "title": "Example Website" }`
- Get only the title of all bookmarks - `{ "title": 1, "_id": 0 }` (Projection)
- Find all the bookmarks that have the tag `Technology` - `{ "tags": "Technology" }`