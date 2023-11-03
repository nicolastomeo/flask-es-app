import logging
import random

from elasticsearch import Elasticsearch, ConnectionError
from flask import Flask, jsonify, render_template

from config import Config
from load_index import load_index
from search_service import SearchService, AggOps

app = Flask(__name__)
app.config.from_object(Config)
app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL'])
app.search_service = SearchService(app.elasticsearch, 'my_index')
app.logger.setLevel(logging.INFO)
load_index(app.elasticsearch, app.logger)

GENDERS = ['M', 'F']
AGG_OPS = ['avg', 'min', 'max']


@app.route("/")
def hello_world():
    return render_template('index.html')


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


@app.route("/docs")
def get_docs():
    ret = app.elasticsearch.search(index="my_index", body={'query': {'match_all': {}}})
    return [{'_id': doc['_id'], **doc['_source']} for doc in ret.body['hits']['hits']]


@app.route("/docs/count")
def get_docs_count():
    ret = app.elasticsearch.count(index='my_index')
    return {'count': ret['count']}


@app.route("/docs", methods=['POST'])
def post_doc():
    lines = []
    with open("words", 'r') as f:
        for line in f:
            lines.append(line[:-1])
    nickname = lines[random.randrange(len(lines))]
    gender = GENDERS[random.randrange(len(GENDERS))]
    age = random.randrange(100)
    doc = {"nickname": nickname, "gender": gender, "age": age}
    ret = app.elasticsearch.index(index="my_index",
                                  document=doc)
    return {"_id": ret.body['_id'], **doc}


@app.route("/docs-100", methods=['POST'])
def post_docs_100():
    for i in range(100):
        post_doc()
    return {"status": "ok"}


@app.route("/docs/gender/<agg_op>", methods=['GET'])
def get_gender_agg(agg_op: str):
    return app.search_service.get_agg_by_gender(AggOps[agg_op.upper()])
