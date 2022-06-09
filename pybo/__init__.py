from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app(main_views=None):
    app = Flask(__name__)
    app.config.from_object(config)
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views, home_views, product_views, review_views,map_view, comment_views, mypage_views, answers_views, questions_views, support_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(home_views.bp)
    app.register_blueprint(product_views.bp)
    app.register_blueprint(review_views.bp)
    app.register_blueprint(map_view.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(answers_views.bp)
    app.register_blueprint(questions_views.bp)
    app.register_blueprint(support_views.bp)


    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 마크다운
    Markdown(app, extensions=['nl2br', 'fenced_code'])
    return app

    return app