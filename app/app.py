import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask_cors import CORS
from flask import Flask, request, render_template
from gevent.wsgi import WSGIServer

from lib.mode import get_by_mode
from lib.readme import readme

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
	return render_template('index.html', readme=readme)

def route(mode, request):
	args = {
		'pool': request.args.get('pool'),
		'selection': request.args.get('selection'), 
		'top_selection': request.args.get('top_selection'),
		'random_selection': request.args.get('random_selection'),  
		'scoring_method': request.args.get('scoring-method'), 
		'score_by_integral_product': request.args.get('score-by-integral-product'), 
		'score_by_integral_sum': request.args.get('score-by-integral-sum'), 
		'score_by_mean_geometric': request.args.get('score-by-mean-geometric'), 
		'score_by_mean_arithmetic': request.args.get('score-by-mean-arithmetic'), 
		'score_threshold': request.args.get('score-threshold'),
		'unweighted': request.args.get('unweighted'), 
		'unstressed': request.args.get('unstressed'),
		'exclude_real': request.args.get('exclude-real')
	}
	response = get_by_mode(mode=mode, interface='api', args=args)
	return json.dumps(response, ensure_ascii=False)

@app.route('/random')
def random_route():
	return route('random', request)

@app.route('/top')
def top_route():
	return route('top', request)

if __name__ == "__main__":
	http_server = WSGIServer(('0.0.0.0', int(os.getenv("PORT", 5000))), app)
	http_server.serve_forever()