from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Questions, Answers
from pybo.views.auth_views import login_required

bp = Blueprint('answers', __name__, url_prefix='/answers')


@bp.route('/create/<int:questions_id>', methods=('POST',))
@login_required
def create(questions_id):
    form = AnswerForm()
    questions = Questions.query.get_or_404(questions_id)
    if form.validate_on_submit():
        content = request.form['content']
        answers = Answers(content=content, create_date=datetime.now(), user=g.user)
        questions.answers_set.append(answers)
        db.session.commit()
        return redirect('{}#answers_{}'.format(
            url_for('questions.detail', questions_id=questions_id), answers.id, user=g.user))
    return render_template('questions/questions_detail.html', questions=questions, form=form, user=g.user)


@bp.route('/modify/<int:answers_id>', methods=('GET', 'POST'))
@login_required
def modify(answers_id):
    answers = Answers.query.get_or_404(answers_id)
    if g.user != answers.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('questions.detail', questions_id=answers.questions.id, user=g.user))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answers)
            answers.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answers_{}'.format(
                url_for('questions.detail', questions_id=answers.questions.id), answers.id, user=g.user))
    else:
        form = AnswerForm(obj=answers)
    return render_template('answersanswersanswers/answersanswersanswers_form.html', form=form, user=g.user)


@bp.route('/delete/<int:answers_id>')
@login_required
def delete(answers_id):
    answers = Answers.query.get_or_404(answers_id)
    questions_id = answers.questions.id
    if g.user != answers.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answers)
        db.session.commit()
    return redirect(url_for('question.detail', questions_id=questions_id, user=g.user))


@bp.route('/vote/<int:answers_id>/')
@login_required
def vote(answers_id):
    answers = Answers.query.get_or_404(answers_id)
    if g.user == answers.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        answers.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answers_{}'.format(
                url_for('question.detail', questions_id=answers.questions.id), answers.id, user=g.user))
