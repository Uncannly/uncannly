import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask_cors import CORS
from flask import Flask, request, render_template
from gevent.wsgi import WSGIServer

from lib.mode import get_by_mode
from lib.readme import readme
from lib.case_conversion import snake_to_kebab
from lib.options import pool_default, pool_max

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
  return render_template('index.html',
    readme=readme, pool_default=pool_default, pool_max=pool_max
  )

def route(mode, request):
  args = {}
  options = [
    'pool', 'selection', 'top_selection', 'random_selection', 'scoring_method',
    'score_by_integral_product', 'score_by_integral_sum', 
    'score_by_mean_geometric', 'score_by_mean_arithmetic', 'score_threshold',
    'unweighted', 'unstressed', 'exclude_real'
  ]
  for option in options:
    args[option] = request.args.get(snake_to_kebab(option))
  response = get_by_mode(mode=mode, interface='api', args=args)
  return json.dumps(response, ensure_ascii=False)

@app.route('/random')
def random_route():
  return route('random', request)

@app.route('/top')
def top_route():
  return route('top', request)

if __name__ == "__main__":
  if os.getenv("PORT") == None:
    app.debug = True
  http_server = WSGIServer(('0.0.0.0', int(os.getenv("PORT", 5000))), app)
  http_server.serve_forever()