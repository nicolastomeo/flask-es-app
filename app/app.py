from elasticsearch import Elasticsearch, ConnectionError
from flask import Flask, jsonify

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL'])


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/health")
def health():
    status = "not ok"
    status_code = 503
    try:
        if app.elasticsearch.cat.health():
            status = "ok"
            status_code = 200
    except ConnectionError:
        app.logger.exception("Elastic healthcheck failed")
    return jsonify({"status": status}), status_code
