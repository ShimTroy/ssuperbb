from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import union

from .. import db
from ..models import Product
from ..forms import QuestionForm, AnswerForm

from pybo.views.auth_views import login_required


bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/heyroo/')
def heyroo():
    category = 'heyroo'
    page = request.args.get('page', type=int, default=1)  # 페이지
    product_list = Product.query.filter(Product.category == category).order_by(Product.id.desc(), Product.create_date.desc())
    product_list = product_list.paginate(page, per_page=12)
    return render_template('product/product_list.html', product_list=product_list, user=g.user, category=category)

@bp.route('/youus/')
def youus():
    category = 'youus'
    page = request.args.get('page', type=int, default=1)  # 페이지
    product_list = Product.query.filter(Product.category == category).order_by(Product.id.desc(), Product.create_date.desc())
    product_list = product_list.paginate(page, per_page=12)
    return render_template('product/product_list.html', product_list=product_list, user=g.user, category=category)

@bp.route('/sselect/')
def sselect():
    category = 'sselect'
    page = request.args.get('page', type=int, default=1)  # 페이지
    product_list = Product.query.filter(Product.category == category).order_by(Product.id.desc(), Product.create_date.desc())
    product_list = product_list.paginate(page, per_page=12)
    return render_template('product/product_list.html', product_list=product_list, user=g.user, category=category)

@bp.route('/minist/')
def minist():
    category = 'minist'
    page = request.args.get('page', type=int, default=1)  # 페이지
    product_list = Product.query.filter(Product.category == category).order_by(Product.id.desc(), Product.create_date.desc())
    product_list = product_list.paginate(page, per_page=12)
    return render_template('product/product_list.html', product_list=product_list, user=g.user, category=category)

@bp.route('/detail/<int:product_id>/')
def detail(product_id):
    form = AnswerForm()
    product = Product.query.get_or_404(product_id)
    category = product.category
    product_list = Product.query.filter(Product.category == category).filter(Product.id != product_id).order_by(Product.id.desc(), Product.create_date.desc())
    return render_template('product/product_detail.html', product=product, form=form, user=g.user, product_list=product_list, category=category)

@bp.route('/vote/<int:product_id>/')
@login_required
def vote(product_id):
    _product = Product.query.get_or_404(product_id)
    if g.user == _product.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _product.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('product.detail', product_id=product_id))