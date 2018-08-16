import json
import os

from flask import Flask, request, render_template
# pylint: disable=import-error
from flask_assets import Environment, Bundle

from lib.mode import get_by_mode
from lib.readme import README
from lib.conversion import snake_to_kebab, kebab_to_space
from lib.options import POOL_DEFAULT, POOL_MAX, TOO_FEW_MESSAGE, \
    NO_WORDS_MESSAGE, MAX_WORD_LENGTH

# pylint: disable=invalid-name
app = Flask(__name__)

assets = Environment(app)
assets.url = app.static_url_path
assets.directory = app.static_folder
assets.manifest = None
assets.cache = False
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

# pylint: disable=redefined-outer-name
def route(mode, request):
    args = {}
    options = [
        'pool', 'selection', 'top_selection', 'random_selection', 'scoring_method',
        'score_by_integral_product', 'score_by_integral_sum',
        'score_by_mean_geometric', 'score_by_mean_arithmetic', 'score_threshold',
        'unweighted', 'unstressed', 'exclude_real', 'ignore_position', 'ignore_length',
        'min_length', 'max_length', 'ignore_syllables'
    ]
    for option in options:
        args[option] = request.args.get(snake_to_kebab(option))
    response = get_by_mode(mode=mode, interface='api', args=args)
    return json.dumps(response, ensure_ascii=False)
# pylint: enable=redefined-outer-name

@app.route('/random')
def random_route():
    return route('random', request)

@app.route('/top')
def top_route():
    return route('top', request)
