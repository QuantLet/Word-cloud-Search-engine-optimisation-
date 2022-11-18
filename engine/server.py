import json

from flask import Flask, request
import logging

from SearchEngine import SearchEngine
from indexers.Meilisearch import Meilisearch

app = Flask(__name__)

search_driver = Meilisearch()
engine = SearchEngine(search_driver)

@app.route('/search', methods=['GET'])
def search():
    results = engine.search(request.args.get("q"))
    ids = [result['courselet_id'] for result in results]
    response = { 'status': 200, 'courseletIds': ids }
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

@app.route('/index', methods=['POST'])
def index_one():
    courselet_id = request.json["courselet_id"]
    pdf_url = request.json["pdf_url"]
    success, data = engine.index(courselet_id, pdf_url)
    if success:
        status = 200
    else:
        status = 417

    return app.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=8080)