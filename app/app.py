import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask_cors import CORS
from flask import Flask, request, render_template
from flask_assets import Environment, Bundle
from gevent.wsgi import WSGIServer

from lib.mode import get_by_mode
from lib.readme import README
from lib.conversion import snake_to_kebab, kebab_to_space
from lib.options import POOL_DEFAULT, POOL_MAX, TOO_FEW_MESSAGE, \
  NO_WORDS_MESSAGE, MAX_WORD_LENGTH

app = Flask(__name__)
CORS(app)

assets = Environment(app)
assets.url = app.static_url_path
assets.directory = app.static_folder
assets.manifest = None
assets.cache = False
assets.append_path(os.path.join('app', 'styles'))
scss = Bundle('styles.scss', filters='pyscss', output='app.css')
assets.register('scss_all', scss)

@app.route('/')
def root():
  return render_template('index.html',
                         readme=README, 
                         pool_default=POOL_DEFAULT, 
                         pool_max=POOL_MAX,
                         too_few_message=TOO_FEW_MESSAGE, 
                         no_words_message=NO_WORDS_MESSAGE,
                         max_word_length=MAX_WORD_LENGTH,
                         kebab_to_space=kebab_to_space)

def route(mode, request):
  args = {}
  options = [
    'pool', 'selection', 'top_selection', 'random_selection', 'scoring_method',
    'score_by_integral_product', 'score_by_integral_sum', 
    'score_by_mean_geometric', 'score_by_mean_arithmetic', 'score_threshold',
    'unweighted', 'unstressed', 'exclude_real', 'ignore_position', 'ignore_length',
    'min_length', 'max_length'
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