from flask import render_template, request, flash, Blueprint, current_app, g
from aweblog.extensions import db
from aweblog.models import Post, Reply
from aweblog.forms import CommentForm
from sqlalchemy import or_
from aweblog.models import Comment
import datetime
from aweblog.utils import redirect_back
#from aweblog.extensions import cache

post_app = Blueprint('post', __name__)


@post_app.before_request
def get_common_data():
    g.post_cn = current_app.config['POST_COUNT']
    catalog_cn = current_app.config['CATALOG_COUNT']
    recent_post_cn = current_app.config['RECENT_POST_COUNT']
    recent_comment_cn = current_app.config['RECENT_COMMENT_COUNT']

    g.catalogs = list(db.session.execute(
        'select * from (select catalog,count(1) from post group by catalog order by 2 desc) limit %s' % catalog_cn))
    g.recent_posts = list(db.session.execute(
        'select * from (select title,content,id from post  order by timestamp desc) limit %s' % recent_post_cn))
    g.recent_comments = list(db.session.execute(
        'select * from (select author,content,post_id from comment order by timestamp desc) limit %s' % recent_comment_cn))


@post_app.route('/')
# 首次会变慢 之后加载速度 14~18ms --->4~5ms
#@cache.cached(query_string=True, timeout=10 * 60)
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, g.post_cn, error_out=False)
    posts = pagination.items
    return render_template('aweblog/post/post.html', posts=posts, pagination=pagination, catalogs=g.catalogs,
                           recent_posts=g.recent_posts, recent_comments=g.recent_comments)


@post_app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', 1, type=int)
    key_word = request.args.get('key_word')
    if not key_word:
        show_posts = Post.query.order_by(Post.timestamp.desc())
    else:
        show_posts = Post.query.filter(
            or_(Post.content.like("%" + key_word + "%"), Post.title.like("%" + key_word + "%")))
    pagination = show_posts.paginate(page, g.post_cn, error_out=False)
    return render_template('aweblog/post/post.html', posts=pagination.items, pagination=pagination, catalogs=g.catalogs,
                           recent_posts=g.recent_posts, recent_comments=g.recent_comments)


@post_app.route('/catalog', methods=['GET'])
def catalog():
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', 1, type=str)
    show_posts = Post.query.filter(Post.catalog == name)
    pagination = show_posts.paginate(page, g.post_cn, error_out=False)
    return render_template('aweblog/post/post.html', posts=pagination.items, pagination=pagination, catalogs=g.catalogs,
                           recent_posts=g.recent_posts, recent_comments=g.recent_comments)


@post_app.route('/post_detail', methods=['GET', 'POST'])
def post_detail():
    page = request.args.get('page', 1, type=int)
    comment_form = CommentForm()
    post_id = request.args.get('id', 1, type=int)
    post_details = Post.query.get(post_id)
    post_details.read_count = post_details.read_count + 1
    db.session.add(post_details)
    db.session.commit()
    pagination = Comment.query.filter(Comment.post_id == post_id).order_by(
        Comment.timestamp.desc()).paginate(page, g.post_cn, error_out=False)
    comment_objs = pagination.items
    cmt_ids = []
    cmt_contents = []
    for i in comment_objs:
        cmt_ids.append(i.id)
        cmt_contents.append(i.content)
    reply_content = []
    for i in cmt_ids:
        old_reply = Reply.query.filter(Reply.comment_id == i).first()
        if old_reply:
            reply_content.append(old_reply.content)
        else:
            reply_content.append(None)
    reply_cmt_rel = dict(zip(comment_objs, reply_content))
    if comment_form.validate_on_submit():
        content = comment_form.content.data
        comment = Comment(author='lw', content=content, email='1429670276@qq.com', site='www.unknow.com',
                          is_admin=True, qualified=True, timestamp=datetime.datetime.utcnow(), post_id=post_id,
                          )
        db.session.add(comment)
        db.session.commit()
        flash('提交成功')
        return redirect_back()
    return render_template('aweblog/post/post_detail.html', post_detail=post_details, catalogs=g.catalogs,
                           recent_posts=g.recent_posts, recent_comments=g.recent_comments, comment_form=comment_form,
                           comments=comment_objs, reply_cmt_rel=reply_cmt_rel, pagination=pagination)


@post_app.route('/back', methods=['GET'])
def back():
    return redirect_back()
