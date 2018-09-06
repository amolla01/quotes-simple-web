# quotes

Simple web server for serving quotes of famous people.

## Dev

Run app:

```bash
python -m quotes
```


Run mongo:

```bash
docker run -d --name mongo -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=test1234 -p 27017:27017 mongo
```