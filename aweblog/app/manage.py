from flask import Blueprint, render_template, request, flash, jsonify, current_app
from aweblog.models import Comment, Post, Reply
from aweblog.extensions import db
from aweblog.utils import redirect_back
from aweblog.forms import PostForm
from flask_login import login_required
import datetime
#from aweblog.extensions import cache

manage_app = Blueprint('manage', __name__)


@manage_app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    post_cn = current_app.config['POST_COUNT']
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, post_cn, error_out=False)
    posts = pagination.items
    return render_template('aweblog/manage/post_list.html',
                           posts=posts, datetime=datetime, pagination=pagination)


@manage_app.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    post_id = request.args.get('post_id')
    record = Post.query.get(post_id)
    db.session.delete(record)
    db.session.commit()
    return redirect_back()


@manage_app.route('/edit_post', methods=['GET','POST'])
@login_required
def edit_post():
    post_id = request.args.get('post_id')
    post = Post.query.get(post_id)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        catalog_id = form.catalog.data
        custom_catalog = form.custom_catalog.data
        catalog = form.choices_dict[catalog_id]
        if custom_catalog:
            catalog = custom_catalog
        content = form.content.data
        update_post = Post(title=title, content=content, catalog=catalog)
        db.session.add(update_post)
        db.session.commit()
        flash('修改成功')
    form.title.data = post.title
    form.catalog.data = post.catalog
    form.content.data = post.content

    return render_template('aweblog/manage/new_post.html', form=form)


@manage_app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        catalog_id = form.catalog.data
        custom_catalog = form.custom_catalog.data
        catalog = form.choices_dict[catalog_id]
        if custom_catalog:
            catalog = custom_catalog
        content = form.content.data
        create_post = Post(title=title, content=content, catalog=catalog)
        db.session.add(create_post)
        db.session.commit()
        flash('创建成功')
    #cache.clear()
    return render_template('aweblog/manage/new_post.html', form=form)


@manage_app.route('/delete_comment', methods=['GET', 'POST'])
@login_required
def delete_comment():
    comment_id = request.args.get('comment_id')
    cmt = Comment.query.get(comment_id)
    reply = Reply.query.filter(Reply.comment_id == comment_id).first()
    db.session.delete(cmt)
    if reply:
        db.session.delete(reply)
    db.session.commit()
    return jsonify(True)


@manage_app.route('/reply_comment', methods=['POST'])
@login_required
def reply_comment():
    comment_id = request.args.get('comment_id')
    reply_content = request.form.get('content')
    # 0新增 1修改
    action = request.args.get('action')
    if action == '0':
        reply = Reply(content=reply_content, comment_id=comment_id)
        db.session.add(reply)
        flash('回复成功')
    if action == '1':
        reply = Reply.query.filter(Reply.comment_id == comment_id).first()
        reply.content = reply_content
        flash('修改成功')
    db.session.commit()
    return redirect_back()


@manage_app.route('/delete_reply', methods=['GET', 'POST'])
@login_required
def delete_reply():
    comment_id = request.args.get('comment_id')
    reply = Reply.query.filter(Reply.comment_id == comment_id).first()
    db.session.delete(reply)
    db.session.commit()
    return jsonify(True)


@manage_app.route('/sync_like_cn', methods=['GET', 'POST'])
def sync_like_cn():
    post_id = request.args.get('post_id')
    love_cn_add = request.args.get('love_cn_add')
    post_obj = Post.query.get(post_id)
    post_obj.love_count = love_cn_add
    db.session.add(post_obj)
    db.session.commit()
    return jsonify(True)


@manage_app.route('/get_reply_data', methods=['GET'])
def get_reply_data():
    cmt_id = request.args.get('comment_id')
    reply_obj = Reply.query.filter(Reply.comment_id == cmt_id).first()
    return jsonify(reply_obj.content)
