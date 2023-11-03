# Flask - ElasticSearch app

## Run
```
docker-compose up --build
```
This command starts an ElasticSearch single node (exposed on port 9200) and a Flask app exposed on port 5000.

User could do a POST /docs-100 to load first 100 docs and then just use explorer to access http://0.0.0.0:5000/ and visualize the plot.

## Local Development

This project was developed with Python 3.11 and Poetry.
Install Poetry (configure local virtualenv is recommended too) and then run
```
poetry install
```
to install all dependencies.

Activate poetry virtualenv and then run
```
cd app
FLASK_APP=app.py FLASK_ENV=development flask run
```

to start application.