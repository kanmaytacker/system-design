# Getting started with Elasticsearch

## Installation

Start a new container with the official Elasticsearch image:

```bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

Start a new container with the official Kibana image:

```bash
docker pull docker.elastic.co/kibana/kibana:8.12.2
docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2
```
