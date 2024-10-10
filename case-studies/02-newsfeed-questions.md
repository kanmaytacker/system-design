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
- USERS
    - USER_ID
    - USER_NAME
    - DOB
    - phone
    - email
    - state
    - country
    - create_timestamp
    - update_timestamp
- USER_FEEDS
    - FEED_ID
    - USER_ID
    - FEED_MSG    
    - create_timestamp
- USER_FRIEND_MAP
    - USER_ID
    - FRIEND_ID (USER_ID)
    - create_timestamp
- IMAGES
   - IMAGE_ID
   - IMAGE
   - create_timestamp
- FEED_IMAGE_MAP ( this can be image/Video )
  - FEED_ID
  - IMAGE_ID
  - create_timestamp
```

*Remember you would also need to store the friends of a user to fetch the newsfeed.*

---
## Major operations

**Think of the different screens in the app and the backend APIs that would be required to support them**

Screen - **Newsfeed**
API calls - 
```
- API 1(USER_ID)
- API 2(FEED_ID)
```

Screen - **Profile page**
```
- API 1(USER_ID)
- API 2(Params)
```
---

### Brute force
*Assume all the information can be stored on a single machine.*

**Question**: Write a query to fetch the posts by a user. This will be used to populate the profile page.

**Answer**: SELECT FEED_MSG , IMAGE , a.create_timestamp 
            FROM USER_FEEDS a
            JOIN USER_FRIEND_MAP c
            ON a.USER_ID = c.USER_ID
            LEFT JOIN FEED_IMAGE_MAP b
            ON a.FEED_ID = b.FEED_ID
            WHERE a.USER_ID =? ORDER BY a.create_timestamp DESC ;

**Question**: Write a query to fetch the posts by a user's friends. This will be used to populate the newsfeed.

**Answer**: SELECT   c.FEED_MSG ,  c.create_timestamp 
            FROM USER_FEEDS a
            JOIN  USER_FRIEND_MAP b
            ON a.USER_ID = b.USER_ID
            JOIN USER_FEEDS c
            ON b.FRIEND_ID = c.USER_ID
            WHERE a.USER_ID =? ORDER BY c.create_timestamp DESC ; 

---
### Estimations - Users

**Question**: How many daily active users (DAUs) does Facebook have? *You don't need to be exact, just provide a rough estimate. You can find this information online and then compare your answer with the actual number.*

**Answer**: ` 2.085 billion`

---

**Question**: How many users can Facebook expect to have in 10 years? *You can assume an arbitrary growth rate based on the current number of users.*

**Answer**: ` 3.5 billion(current users) growing 10% YOY , 38.5 billion users`

---

**Question**: What is the size of a user record in bytes based on the schema you have created?

**Answer**: `USER Entity -  311 bytes`

---

**Question**: How much storage would you need for users in 10 years?

**Formula**: `Total storage = 311 * 38.5 billion = 11.9 TB`

**Answer**: ` `

---

**Question**: Do you need to shard the users table?

**Answer**: `Yes , user table needs sharding `

---

### Sharding

*Assuming that you need to shard the database. This would include the database for users and posts.*

**Question**: `What would be the different candidate keys for sharding?`

**Answer**:
```
- state
- country
```

### Candidate key 1

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- Operation 1
    - Number of hops
- Operation 2
    - Number of hops
```

### Candidate key 2

**Question**: `List down the number of reads and writes required for each operation`

**Answer**:
```
- Operation 1
    - Number of hops
- Operation 2
    - Number of hops
```

**Final choice**: ` `

---state

### Estimations - Posts

*You should have figured by now that the users DB is going to be huge, and it needs to be sharded. However, none of the sharding keys produce optimal results. Let us figure out if the posts table actually needs to be sharded.*


**Question**: What percentage of the daily active users do you think create posts daily?

**Answer**: `65% users are active on daily basis `

---

**Question**: How many posts do you think a user would make in a day?

**Answer**: `5 feeds created by active user per day `

---

**Question**: What is the total number of posts created in a day?

**Formula**: `Total number of posts = 0.65 * 3.5 billion *  5 feeds = 11.3 billion feeds`
**Answer**: ` `

---
**Question**: What is the size of a post in bytes?
*Based on the schema you have created, estimate the size of a post.*

**Answer**: `11.3 billion feeds * `

---
**Question**: What is the total amount of data generated by posts in a day?
**Formula**: `Total data generated = _ * _`
**Answer**: ` `

---
**Question**: How much data would you need to store for posts from the last 30 days?

**Answer**: ` `

---
**Question**: Do you need to shard the posts table? Specifically for the newsfeed use case where you don't need all the posts, only the recent ones.

**Answer**: ` `

---
### Final solution

>News feed is supposed to show only recent posts from a friend. You don’t expect to see a year old post in your news feed. Let’s assume you only need to show posts made in the last 30 days. In that case, you don’t need to worry about sharding the posts table and rather can just use a secondary database to store the recent posts. 

Given the above, write the flows for each of the operations you have listed above.

---

**Operation name**: ` `
**Flow**:
```
1. Step 1
2. Step 2
3. Step 3
...
```

---

**Operation name**: ` `
**Flow**:
```
1. Step 1
2. Step 2
3. Step 3
...
```

---
