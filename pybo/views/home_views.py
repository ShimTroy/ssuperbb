from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db
from ..models import Product
from ..forms import QuestionForm, AnswerForm

from pybo.views.auth_views import login_required

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def _home():
    # return render_template('map.html', user=g.user)
    product_list = Product.query.order_by(Product.create_date.desc())
    return render_template('home/home.html', user=g.user, product_list=product_list)