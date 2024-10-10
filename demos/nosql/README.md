# SQL vs NoSQL databases

This folder contains a set of demos comparing the SQL and NoSQL databases.
You can find the following demos:

1. [The bookmarks schema in Postgres](./bookmarks.sql)
2. [Key-value store - Redis](./redis.md)
3. [MongoDB](./mongo.md)
4. [Columnar database - ClickHouse](./clickhouse.md)

---
## Getting the database servers running

The demos are designed to run on your local machine using `Docker Compose`.
You can find the `docker-compose.yml` [here](./docker-compose.yml).

> If you don't have Docker or Docker Compose installed, follow the instructions [here](https://docs.docker.com/compose/install/).

To start the database servers, run the following command from this directory:

```bash
docker-compose up -d
```


> You should have Docker daemon running on your machine. Verify it by running `docker info`.

This command will start the following services:
- Postgres
- Redis
- MongoDB
- ClickHouse

Verify that the services are running by running:

```bash
docker-compose ps
```
To stop the services, run:

```bash
docker-compose down
```

---
## Postgres

The file [bookmarks.sql](./bookmarks.sql) contains the schema for a bookmarks database. It also contains some sample data.


> The credentials are defined in the `docker-compose.yml` file. The values are:
    - POSTGRES_USER: root
    - POSTGRES_PASSWORD: example
    - POSTGRES_DB: bookmarks


To create the schema and load the data, run the following command:

```bash
docker exec -i postgresdb psql -U root -d bookmarks < bookmarks.sql
```

You should see the following output:

```bash
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 3
INSERT 0 4
INSERT 0 5
```

To connect to the database, run:

```bash
docker exec -it postgresdb psql -U root -d bookmarks
```

Once connected, you can run SQL queries. For example, the following lists all the users by the number of bookmarks they have:

```sql
SELECT u.UserID, u.Username, COUNT(b.BookmarkID) AS bookmarks
FROM users u
LEFT JOIN bookmarks b ON u.UserID = b.UserID
GROUP BY u.UserID
ORDER BY bookmarks DESC;
````

Explore the schema and data to understand how the bookmarks database is structured. Refer to it when comparing with other databases.

---
### NoSQL databases

Your NoSQL database servers should be running as well. Head to the respective files to explore the demos for each database:
- [Redis](./redis.md)
- [MongoDB](./mongo.md)
- [ClickHouse](./clickhouse.md)   