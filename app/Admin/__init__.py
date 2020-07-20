from flask import Blueprint


admin = Blueprint('admin', __name__)

import app.Admin.login
import app.Admin.anime
import app.Admin.ask
import app.Admin.recommend
import app.Admin.user