import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask_cors import CORS
from flask import Flask, request, render_template
from gevent.wsgi import WSGIServer

import random_word, words

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/words')
def words_route():
    probable_words = words.get(
        return_count=request.args.get('return-count'),
        scoring_method=request.args.get('scoring-method'), 
        score_by_integral_product=request.args.get('score-by-integral-product'), 
        score_by_integral_sum=request.args.get('score-by-integral-sum'), 
        score_by_mean_geometric=request.args.get('score-by-mean-geometric'), 
        score_by_mean_arithmetic=request.args.get('score-by-mean-arithmetic'), 
        score_threshold=request.args.get('score-threshold'),
        random_selection=request.args.get('random-selection'), 
    	unweighted=request.args.get('unweighted'), 
        exclude_real=request.args.get('exclude-real'),
        # pool_count=request.args.get('pool_count')
    ) 
    return json.dumps(probable_words, ensure_ascii=False)

@app.route('/random-word')
def random_word_route():
    word = random_word.get(
        unweighted=request.args.get('unweighted'), 
        exclude_real=request.args.get('exclude-real')
    )
    return json.dumps(word, ensure_ascii=False)

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(os.getenv("PORT", 5000))), app)
    http_server.serve_forever()