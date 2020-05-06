from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor

# from flask_caching import Cache

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()


# cache = Cache(config={'CACHE_TYPE': 'simple'})


@login_manager.user_loader
def load_user(user_id):
    from aweblog.models import Admin

    return Admin.query.get(user_id)


login_manager.login_view = 'auth.login'
# login_manager.login_message = '请登录后再操作'
login_manager.login_message_category = 'warning'
