from flask import Blueprint


admin = Blueprint('admin', __name__)

import app.Admin.login
import app.Admin.anime