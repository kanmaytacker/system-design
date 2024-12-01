# Facebook Newsfeed Case Study

In this worksheet, the goal is to come up with the high level design of the Facebook newsfeed. Users can come to the newsfeed and see posts by their friends. 

In practice, these could also be sponsored posts or posts from pages that the user follows. However, for the sake of simplicity, we will only consider posts from friends in this case study. Your goal should be to create a scalable system that can handle the large number of users and posts that Facebook has.

![Facebook newsfeed](https://www.usatoday.com/gcdn/-mm-/ffa8370e75f659a649843416166c5b2d294a1cdb/c=0-2-580-328/local/-/media/2017/05/04/USATODAY/usatsports/newsfeed_large.png?width=1200&disable=upscale&format=pjpg&auto=webp)

Along with the newsfeed, Facebook also has a profile page where you can see the posts made by the user along with user details.

![Facebook profile page](https://i.insider.com/4e79fde4eab8ea821b000029?width=750&format=jpeg&auto=webp)

## Functional Requirements

- User should be able to see posts made by their friends on the newsfeed.
- Users should be able to see the posts made by other users on their profile page.
- The newsfeed should display recent posts from friends, ordered by time.

## Schema Design

**Task** - Come up with a basic data schema for the requirements of the newsfeed and profile page.

### Entities and attributes

List all the entities that you think are necessary for the newsfeed and profile page

```
- User
    - User ID
    - Name
    - Email
    - Relationship status
    - Last active
- User Friends
    - User ID
    - Friend ID
- Post
    - Post ID
    - User ID
    - Content
    - Created Timestamp
    - Updated Timestamp

```

*Remember you would also need to store the friends of a user to fetch the newsfeed.*

---
## Major operations

**Think of the different screens in the app and the backend APIs that would be required to support them**

Screen - **Newsfeed**
API calls - 
```
- GetFriendsList(user_id): Get the user's friend list
- GetFriendsPosts(user_id, pagination): Get recent posts made by the user's friends. Pagination used to enhance readablility and navigation.

```

Screen - **Profile page**
```
- GetUserProfile(user_id): Get the user's profile information
- GetUserPosts(user_id, pagination): Get the user's own posts. Pagination used to enhance readablility and navigation.


```
---

### Brute force
*Assume all the information can be stored on a single machine.*

**Question**: Write a query to fetch the posts by a user. This will be used to populate the profile page.

**Answer**: ` SELECT * FROM Posts WHERE user_id = <user_id> ORDER BY timestamp DESC LIMIT x OFFSET y; `

**Question**: Write a query to fetch the posts by a user's friends. This will be used to populate the newsfeed.

**Answer**: ` SELECT * FROM User_friends a JOIN Posts b ON a.user_id = <user_id> AND b.user_id = a.friend_id AND b.timestamp < NOW - 30 days LIMIT x OFFSET y `

---
### Estimations - Users

**Question**: How many daily active users (DAUs) does Facebook have? *You don't need to be exact, just provide a rough estimate. You can find this information online and then compare your answer with the actual number.*

**Answer**: ` As of September 2024, Facebook has about 2.11 billion daily active users (DAUs). This is a 5.5% increase from the previous year `

---

**Question**: How many users can Facebook expect to have in 10 years? *You can assume an arbitrary growth rate based on the current number of users.*

**Answer**: ` In 10 years, assuming a constant growth rate of 5.5%, Facebook can expect to have approximately 3.6 billion daily active users (DAUs). ​​`

---

**Question**: What is the size of a user record in bytes based on the schema you have created?

**Answer**: ` ID (4 bytes) + Name (~100 bytes) + Email (~100 bytes) + Relationship status (1 byte) + Last active (4 bytes) = 209 bytes. `

---

**Question**: How much storage would you need for users in 10 years?

**Formula**: ` Total storage = Number of users * Size of user record `

**Answer**: ` 3.6 billion * 209 bytes = 752.4 gigabytes `

---

**Question**: Do you need to shard the users table?

**Answer**: ` Yes, you would need to shard the users table as it would be too large to fit on a single machine. `

---

### Sharding

*Assuming that you need to shard the database. This would include the database for users and posts.*

**Question**: `What would be the different candidate keys for sharding?`

**Answer**:
```
- Candidate key 1: User_ID
- Candidate key 2: Post_ID
```

### Candidate key 1

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- Operation 1: Fetch user’s profile page (Fetch the user details and posts)
    - Number of hops: 1 (single shard based on user_id)
- Operation 2: Fetch user’s newsfeed
    - Number of hops: Multiple (as friend posts may be on different shards)
```

### Candidate key 2

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- Operation 1: Fetch user’s profile page
    - Number of hops: 1 (single shard based on post_id for posts)
- Operation 2: Fetch user’s newsfeed
    - Number of hops: Multiple (as friends' posts may be on different shards)
```

**Final choice**: ` User_ID would be the better choice for sharding as it would reduce the number of hops required for fetching the user's profile page and other user-centric operations. `

---

### Estimations - Posts

*You should have figured by now that the users DB is going to be huge, and it needs to be sharded. However, none of the sharding keys produce optimal results. Let us figure out if the posts table actually needs to be sharded.*


**Question**: What percentage of the daily active users do you think create posts daily?

**Answer**: ` 1% `

---

**Question**: How many posts do you think a user would make in a day?

**Answer**: ` 2 `

---

**Question**: What is the total number of posts created in a day?

**Formula**: `Total number of posts = DAUs * Percentage of DAUs creating posts * Number of posts per user ` 
**Answer**: ` 3.6 billion * 1% * 2 = 72 million `

---
**Question**: What is the size of a post in bytes?
*Based on the schema you have created, estimate the size of a post.*

**Answer**: ` Post ID (4 bytes) + User ID (4 bytes) + Content (~200 bytes) + Created Timestamp (8 bytes) + Updated Timestamp (8 bytes) = 224 bytes`

---
**Question**: What is the total amount of data generated by posts in a day?
**Formula**: ` Total data generated = Total number of posts * Size of post `
**Answer**: ` 72 million * 224 bytes = 16 GB `

---
**Question**: How much data would you need to store for posts from the last 30 days?

**Answer**: ` 16 GB * 30 = 480 GB`

---
**Question**: Do you need to shard the posts table? Specifically for the newsfeed use case where you don't need all the posts, only the recent ones.

**Answer**: ` No, you don't need to shard the posts table for the newsfeed use case. You can store the recent posts in a separate database and fetch them from there. `

---
### Final solution

>News feed is supposed to show only recent posts from a friend. You don’t expect to see a year old post in your news feed. Let’s assume you only need to show posts made in the last 30 days. In that case, you don’t need to worry about sharding the posts table and rather can just use a secondary database to store the recent posts. 

Given the above, write the flows for each of the operations you have listed above.

---

**Operation name**: `GetFriendsPosts `
**Flow**:
```
1. Fetch the user's list of friends from the user's shard.
2. For each friend, fetch the recent posts made by the friend from the secondary database.
```

---

**Operation name**: ` Get profile page `
**Flow**:
```
1. Fetch the user's details from the user's shard.
2. Fetch the user's posts from the secondary database.
```

---
