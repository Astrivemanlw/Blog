from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from aweblog.extensions import db


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 20)])
    catalog = SelectField('分类', coerce=int, default=1)
    custom_catalog = StringField('新分类', validators=[Length(1, 10)], default="无")
    content = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        rs = list(db.session.execute('select distinct(catalog) from post order by catalog desc'))
        cn = list(db.session.execute('select count(distinct(catalog)) from post'))[0]
        ids = [i for i in range(1, cn[0] + 1)]
        catalogs = [i[0] for i in rs]
        choices = dict(zip(ids, catalogs))
        self.choices_dict = choices
        self.catalog.choices = [(k, v) for k, v in choices.items()]


class CommentForm(FlaskForm):
    content = TextAreaField('评论', validators=[Length(1, 200)])
    submit = SubmitField()


class ReplyForm(FlaskForm):
    reply = TextAreaField('回复', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='用户名不能为空!'), Length(1, 12)])
    password = StringField('Password', validators=[DataRequired(message='密码不能为空!'), Length(8, 12)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')
