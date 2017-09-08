from flask import Flask, Response
import json
import os
import redis
from rdflib import Graph, URIRef, Literal

import logging

app = Flask(__name__)

logger = None


@app.route('/')
def get_entities():
    host = os.environ.get('host') or "localhost"
    port = int(os.environ.get('port')) or 6379
    db = int(os.environ.get('db')) or 0

    logger.info("Get Redis data from %s using port: %s" % (host, port))

    try:
        graph = Graph()
        logger.info("Reading entities...")

        r = redis.StrictRedis(host=host, decode_responses=True, port=port, db=db)
        for key in r.scan_iter():
            # do something with the key
            if r.type(key) == "hash":
                info = r.hgetall(key)
                for vkey, value in info.items():
                    for item in json.loads(value):
                        if item["literal"]:
                            if "datatype" in item:
                                graph.add((URIRef(item["subject"]),URIRef(item["property"]),Literal(item["object"],datatype=URIRef(item["datatype"]))))
                            else:
                                graph.add((URIRef(item["subject"]), URIRef(item["property"]), Literal(item["object"])))
                        else:
                            graph.add((URIRef(item["subject"]), URIRef(item["property"]), URIRef(item["object"])))

        return Response(graph.serialize(format='nt'), mimetype='text/plain')

    except BaseException as e:
        logger.exception("Failed to read entities!")
        return Response(status=500, response="An error occured during generation of entities: %s" % e)


if __name__ == '__main__':
    # Set up logging
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('redis')

    # Log to stdout
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    logger.setLevel(logging.DEBUG)

    app.run(threaded=True, debug=True, host='0.0.0.0')
