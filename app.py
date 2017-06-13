import math
import os

from PIL import Image
from flask import Flask, request, send_from_directory, abort
app = Flask(__name__, static_url_path='')

IMAGES_ROOT = 'images'


def has_image(name):
    return os.path.isfile(os.path.join(IMAGES_ROOT, name))


def round_up(num):
    return int(math.ceil(num / 10.0)) * 10


def opt_filename(filename, width, height):
    parts = filename.split('.')
    name = ''.join(parts[0:-1])
    ext = parts[-1]
    return '{}_{}x{}.{}'.format(name, width, height, ext)


def opt_image(filename, width, height):
    path = os.path.join(IMAGES_ROOT, filename)
    print(path)
    if not os.path.isfile(path):
        return None

    width = round_up(width)
    height = round_up(height)
    new_filename = opt_filename(filename, width, height)
    new_path = os.path.join(IMAGES_ROOT, new_filename)

    if os.path.isfile(new_path):
        return new_filename

    image = Image.open(path)
    image.thumbnail((width, height))

    image.save(new_path)

    return new_path


@app.route('/<filename>/<int:width>/<int:height>')
def optimise(filename, width, height):
    new_path = opt_image(filename, width, height)
    if not new_path:
        abort(404)

    return '{}images/{}'.format(request.url_root, new_path)


@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)
