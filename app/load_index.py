from logging import Logger

from elasticsearch import Elasticsearch


def load_index(client: Elasticsearch, logger: Logger):
    if not client.indices.exists(index="my_index"):
        client.indices.create(index="my_index",
                              mappings={"properties": {"nickname": {"type": "keyword"},
                                                       "gender": {"type": "keyword"},
                                                       "age": {"type": "float"}}
                                        })
        logger.info("Index created")
    else:
        logger.info("Index already exists")
