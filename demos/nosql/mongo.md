# Mongo queries

## Connect to the database

```bash
 docker exec -it mongodb mongo -u root -p example --authenticationDatabase admin
```

## 2. **Insert Users Data**

Switch to the database (`bookmarks`) and insert the users into the `users` collection:

```javascript
use bookmarks;

db.users.insertMany([
  { "username": "tantia.tope", "email": "tantia.top@example.com" },
  { "username": "sherlock.holmes", "email": "sherlock.holmes@example.com" },
  { "username": "bruce.wayne", "email": "bruce.wayne@example.com" }
]);
```

## 3. **User Queries**

- Get all users:
  ```javascript
  db.users.find({});
  ```

- Get the user with username `tantia.tope`:
  ```javascript
  db.users.find({ "username": "tantia.tope" });
  ```

- Get only the username of all users (Projection):
  ```javascript
  db.users.find({}, { "username": 1, "_id": 0 });
  ```

## 4. **Insert Bookmarks Data**

First, you need to fetch the `userID` from the `users` collection and replace them in the insert query. Here's an example of how to get all the user IDs:

```javascript
db.users.find({}, { "_id": 1 });
```

Once you have the IDs, you can replace the placeholder values and insert the bookmarks:

```javascript
db.bookmarks.insertMany([
  {
    "userID": ObjectId("replace_with_actual_userID_1"), // Replace with actual ObjectId
    "url": "https://www.example.com",
    "title": "Example Website",
    "description": "This is an example website.",
    "createdOn": new Date("2024-07-24T12:00:00Z"),
    "tags": ["Education", "Technology"]
  },
  {
    "userID": ObjectId("replace_with_actual_userID_2"), // Replace with actual ObjectId
    "url": "https://www.news.com",
    "title": "News Website",
    "description": "This is a news website.",
    "createdOn": new Date("2024-07-24T13:00:00Z"),
    "tags": ["News", "Technology"]
  },
  {
    "userID": ObjectId("replace_with_actual_userID_3"), // Replace with actual ObjectId
    "url": "https://www.opensource.org",
    "title": "Open Source",
    "description": "This is an open source community website.",
    "createdOn": new Date("2024-07-24T14:00:00Z"),
    "tags": ["Open Source"]
  }
]);
```

### 5. **Bookmark Queries**

- Get all bookmarks:
  ```javascript
  db.bookmarks.find({});
  ```

- Get the bookmark with the title `Example Website`:
  ```javascript
  db.bookmarks.find({ "title": "Example Website" });
  ```

- Get only the title of all bookmarks (Projection):
  ```javascript
  db.bookmarks.find({}, { "title": 1, "_id": 0 });
  ```

- Find all bookmarks that have the tag `Technology`:
  ```javascript
  db.bookmarks.find({ "tags": "Technology" });
  ```
