# databrowser-redis
Adapter to read config and change requests from the Sesam Databrowser REDIS backend as n-triples (RDF)

[![Build Status](https://travis-ci.org/sesam-community/databrowser-redis.svg?branch=master)](https://travis-ci.org/sesam-community/databrowser-redis)

The service takes the following parameters:

`host = Hostname or IP address for REDIS server (Default = localhost)`

`port = What port the REDIS server is using (Default = 6379)`

`db = Which database to talk to (Default = 0)`

# Known issues

Doesn't support writing data back to the databrowser yet.
