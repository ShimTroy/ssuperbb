from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import QuestionsForm, AnswerForm
from pybo.models import Questions , Answers, User
from pybo.views.auth_views import login_required

bp = Blueprint('support', __name__, url_prefix='/support')

@bp.route('/')
def support():
    # return redirect(url_for('product._heyroo'))
    return render_template('support/ssuport.html',  user=g.user)