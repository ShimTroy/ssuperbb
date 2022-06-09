from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import QuestionsForm, AnswerForm
from pybo.models import Questions , Answers, User
from pybo.views.auth_views import login_required

bp = Blueprint('questions', __name__, url_prefix='/questions')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    questions_list = Questions.query.order_by(Questions.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answers.questions_id, Answers.content, User.username) \
            .join(User, Answers.user_id == User.id).subquery()
        questions_list = questions_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.questions_id == Questions.id) \
            .filter(Questions.subject.ilike(search) |  # 질문제목
                    Questions.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    questions_list = questions_list.paginate(page, per_page=10)
    return render_template('questions/questions_list.html', questions_list=questions_list, page=page, kw=kw, user=g.user)

@bp.route('/detail/<int:questions_id>/')
def detail(questions_id):
    form = AnswerForm()
    questions = Questions.query.get_or_404(questions_id)
    return render_template('questions/questions_detail.html', questions=questions, form=form, user=g.user)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionsForm()
    if request.method == 'POST' and form.validate_on_submit():
        questions = Questions(subject=form.subject.data, content=form.content.data, category=form.category.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(questions)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('questions/questions_form.html', form=form, user=g.user)


@bp.route('/modify/<int:questions_id>', methods=('GET', 'POST'))
@login_required
def modify(questions_id):
    questions = Questions.query.get_or_404(questions_id)
    if g.user != questions.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=questions_id, user=g.user))
    if request.method == 'POST':  # POST 요청
        form = QuestionsForm()
        if form.validate_on_submit():
            form.populate_obj(questions)
            questions.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('questions.detail', question_id=questions_id, user=g.user))
    else:  # GET 요청
        form = QuestionsForm(obj=questions)
    return render_template('questions/questions_form.html', form=form, user=g.user)


@bp.route('/delete/<int:questions_id>')
@login_required
def delete(questions_id):
    questions = Questions.query.get_or_404(questions_id)
    if g.user != questions.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('questions.detail', questions_id=questions_id, user=g.user))
    db.session.delete(questions)
    db.session.commit()
    return redirect(url_for('questions._list'))


@bp.route('/vote/<int:questions_id>/')
@login_required
def vote(questions_id):
    questions = Questions.query.get_or_404(questions_id)
    if g.user == questions.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        questions.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('questions.detail', question_id=questions_id, user=g.user))
