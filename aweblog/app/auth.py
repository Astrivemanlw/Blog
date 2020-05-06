from flask import url_for, flash, render_template, redirect, Blueprint, request
from aweblog.forms import LoginForm
from aweblog.models import Admin
from flask_login import current_user, login_user, logout_user
from aweblog.utils import redirect_back

auth_app = Blueprint('auth', __name__)


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        rs = Admin.query.filter_by(username=username).first()
        if rs:
            if rs.username == username and rs.validate_password(password):
                if rs.username == 'admin':
                    login_user(rs, remember)
                    return redirect_back()
                else:
                    return redirect_back()
            else:
                flash('无效用户名或密码')

        else:
            flash('无效用户名或密码')

    return render_template('aweblog/auth/login.html', form=form)


@auth_app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect_back()
