from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

product_voter = db.Table(
    'product_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), primary_key=True)
)

review_voter = db.Table(
    'review_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('review.id', ondelete='CASCADE'), primary_key=True)
)

questions_voter = db.Table(
    'questions_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('questions_id', db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True)
)

answers_voter = db.Table(
    'answers_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answers_id', db.Integer, db.ForeignKey('answers.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))


# 사용자 정보
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# 상품 정보
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), nullable=False)  # 회사
    subject = db.Column(db.String(), nullable=False)  # 상품명
    content = db.Column(db.String(), nullable=False)  # 가격
    explaination = db.Column(db.String(), nullable=False)  # 설명
    address = db.Column(db.String(), nullable=False)  # 이미지 경로
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('product_set'))
    create_date = db.Column(db.DateTime(), nullable=False)
    voter = db.relationship('User', secondary=product_voter, backref=db.backref('product_voter_set'))


# 후기 정보
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    product = db.relationship('Product', backref=db.backref('review_set', cascade='all, delete-orphan'))
    content = db.Column(db.String(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('review_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=review_voter, backref=db.backref('review_voter_set'))

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), nullable=True, server_default='1')
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('questions_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=questions_voter, backref=db.backref('questions_voter_set'))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    questions = db.relationship('Questions', backref=db.backref('answers_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, server_default='1')
    user = db.relationship('User', backref=db.backref('answers_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answers_voter, backref=db.backref('answers_voter_set'))