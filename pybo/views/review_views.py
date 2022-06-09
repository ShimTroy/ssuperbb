from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Product, Review
from .auth_views import login_required

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/create/<int:product_id>', methods=('POST',))
@login_required
def create(product_id):
    form = AnswerForm()
    product = Product.query.get_or_404(product_id)
    if form.validate_on_submit():
        content = request.form['content']
        review = Review(content=content, create_date=datetime.now(), user=g.user)
        product.review_set.append(review)
        db.session.commit()
        return redirect(url_for('product.detail', product_id=product_id))
    return render_template('product/product_detail.html', product=product, form=form, user=g.user)

@bp.route('/modify/<int:review_id>', methods=('GET', 'POST'))
@login_required
def modify(review_id):
    review = Review.query.get_or_404(review_id)
    if g.user != review.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('product.detail', product_id=review.product.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(review)
            review.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('product.detail', product_id=review.product.id))
    else:
        form = AnswerForm(obj=review)
    return render_template('answer/answer_form.html', form=form, user=g.user)

@bp.route('/delete/<int:review_id>')
@login_required
def delete(review_id):
    review = Review.query.get_or_404(review_id)
    product_id = review.product.id
    if g.user != review.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('product.detail', product_id=product_id))

@bp.route('/vote/<int:review_id>/')
@login_required
def vote(review_id):
    _review = Review.query.get_or_404(review_id)
    if g.user == _review.user:
        flash('본인이 작성한 글은 좋아요 할 수 없습니다')
    else:
        _review.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('product.detail', product_id=_review.product.id))