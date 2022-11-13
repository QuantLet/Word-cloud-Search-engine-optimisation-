The following env variables are needed:

````
MEILISEARCH_MASTER_KEY=""
MEILISEARCH_URL=""
````

Build the docker image:
```
sudo docker build -t search-engine:latest .
```

Run locally:
```
sudo docker run -p 8880:8080 -e MEILISEARCH_URL=http://host.docker.internal:7700  search-engine:latest
```