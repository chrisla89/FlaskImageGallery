import flask
from flask import Flask, render_template, redirect, url_for
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint, flask_swagger_ui

from flaskr.repo import ImgRepo
from flaskr.utils import chunketize

app = Flask(__name__)
repo = ImgRepo()


@app.before_request
def register_repo():
    flask.g.repo = repo


@app.route('/')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/gallery/<string:category>/<int:img_offset>')
def gallery(category, img_offset):
    page_size = 12

    if img_offset % page_size != 0:
        return f"img_offset not divisible by {page_size}", 400

    return render_template('gallery.html', category=category, img_offset=img_offset, chunk_size=6, page_size=page_size)


@app.route('/gallery/<string:category>/')
def gallery_(category):
    return redirect(url_for('gallery', category=category, img_offset=0))


@app.route('/api/galleries')
def api_list_galleries():
    """
    List available categories
    ---
    tags: [gallery-api]
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            type: string
          example: ['Category 01', 'Category 02', 'Some Other Category']
    """
    return repo.categories()


@app.route('/api/gallery/<string:category>')
def api_list_files_in_category(category: str):
    """
    List files for category
    ---
    tags: [gallery-api]
    parameters:
    - name: category
      in: path
      description: category name (case-sensitive)
      type: string
      required: true
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            type: string
          example: ['https://local.example/static/c1_001.jpg',
                    'https://local.example/static/c1_002.jpg',
                    'https://local.example/static/c2_001.jpg']
      404:
        description: Gallery not found
    """
    if category not in repo.categories():
        return "Gallery not found", 404

    return repo.files_in_category(category=category)


@app.route('/swagger.json')
def swagger_json():
    swag = swagger(app)
    swag['info']['version'] = "0.0.1"
    swag['info']['title'] = "My Gallery API"
    return swag


app.jinja_env.filters['chunketize'] = chunketize

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint)
