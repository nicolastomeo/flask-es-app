import os


class Config:
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', "http://localhost:9200")
