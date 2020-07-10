from flask import Blueprint

anime = Blueprint('anime', __name__)

import app.Anime.route
