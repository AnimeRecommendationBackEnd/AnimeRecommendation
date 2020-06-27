from flask import Blueprint,jsonify,request,current_app,session
from app.models import *
from app.utils import *
from app.extensions import r,login_required,send_email
import pickle
import os


user = Blueprint('user', __name__)

import app.User.create
import app.User.login
import app.User.updata

