from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Product

from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Review, Answer, User, question_voter
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required
from sqlalchemy import func

mysql = MySQL()
bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/')
def main():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())

    return render_template('mypage/mypage_writtenquestion.html', user=g.user, product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/writtenquestion')
def writtenquestion():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())
    return render_template('mypage/mypage_writtenquestion.html', user=g.user, product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/recommendproduct')
def recommendproduct():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())
    return render_template('mypage/mypage_recommendproduct.html', user=g.user, product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/recommendquestion')
def recommendquestion():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())
    return render_template('mypage/mypage_recommendquestion.html', user=g.user,product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/writtenreview')
def writtenreview():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())

    return render_template('mypage/mypage_writtenreview.html', user=g.user, product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/writtenanswer')
def writtenanswer():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())

    return render_template('mypage/mypage_writtenanswer.html', user=g.user,product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)

@bp.route('/recommendreview')
def recommendreview():
    product_list = Product.query.order_by(Product.id.desc())
    question_list = Question.query.order_by(Question.create_date.desc())
    answer_list = Answer.query.order_by(Answer.create_date.desc())
    review_list = Review.query.order_by(Review.create_date.desc())

    return render_template('mypage/mypage_recommendreview.html', user=g.user,product_list=product_list, question_list=question_list, review_list=review_list, answer_list=answer_list)
