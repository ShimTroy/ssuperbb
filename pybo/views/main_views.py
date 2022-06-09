from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # return redirect(url_for('product._heyroo'))
    return redirect(url_for('home._home'))