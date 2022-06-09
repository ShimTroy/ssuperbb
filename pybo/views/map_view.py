from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db
from ..models import Question, User
from ..forms import QuestionForm, AnswerForm

from pybo.views.auth_views import login_required

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def map():
    return render_template('map/map.html', user=g.user)