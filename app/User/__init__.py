from flask import Blueprint,jsonify,request,current_app
from app.models import *
from app.utils import *
from app.extensions import r,login_required
import pickle
import os


user = Blueprint('user', __name__)

import app.User.create
import app.User.login
import app.User.updata

