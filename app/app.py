import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask_cors import CORS
from flask import Flask, request
from gevent.wsgi import WSGIServer

from lib.api import random_probable_word, most_probable_words

app = Flask(__name__)
CORS(app)

@app.route('/words')
def words():
    style = request.args.get('style') # sorted or random
    filter = request.args.get('filter') # by averaging, by continued product, or none
    weighted_by_frequency = request.args.get('weighted_by_frequency') # true or false
    include_real_words = request.args.get('include_real_words') # true or false
    return_count = request.args.get('return_count') # how many words to return
    # pool_count = request.args.get('pool_count') # how many words to generate to draw from

    weighted_by_frequency = False if weighted_by_frequency == 'false' else True
    include_real_words = False if include_real_words == 'false' else True

    words = most_probable_words.get(
    	style=style, 
    	filter=filter, 
    	weighted_by_frequency=weighted_by_frequency, 
        include_real_words=include_real_words,
    	return_count=return_count
    ) 
    return json.dumps(words)

@app.route('/random-word')
def random_word():
    weighted_by_frequency = request.args.get('weighted_by_frequency') # true or false
    include_real_words = request.args.get('include_real_words') # true or false

    weighted_by_frequency = False if weighted_by_frequency == 'false' else True
    include_real_words = False if include_real_words == 'false' else True

    word = random_probable_word.get(
        weighted_by_frequency=weighted_by_frequency,
        include_real_words=include_real_words
    )
    return json.dumps(word, ensure_ascii=False)

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(os.getenv("PORT", 5000))), app)
    http_server.serve_forever()