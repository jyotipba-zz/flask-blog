from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from my_blog import db
from my_blog.models import Post,Comment,User
from my_blog.posts.forms import CreatePost, CommentPostForm

posts = Blueprint('posts' , __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePost()
    if form.validate_on_submit():
        user = Post(body=form.Body.data, title= form.Title.data, author  = current_user)
        db.session.add(user)
        db.session.commit()
        flash("Dear {}, your post is submitted".format(current_user.username) , 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='new_post', form=form)


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html' , title = post.title, post = post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.Title.data
        post.body = form.Body.data
        db.session.commit()
        flash("Your post has been updated", 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':

        form.Title.data = post.title
        form.Body.data = post.body

    return render_template('new_post.html', title='update', form=form)

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", 'success')
    return redirect(url_for('main.home'))





@posts.route('/post/<int:post_id>/post_comment', methods=['POST', 'GET'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentPostForm()
    if form.validate_on_submit():
        comment = Comment(comment_id= post_id, c_body = form.body.data, commentator  = current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted", 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    return render_template('post_comment.html' , post = post, title = 'post_comment' , form = form)


@posts.route('/post/<int:post_id>/show_comment', methods=['POST', 'GET'])
@login_required
def show_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.comment_id == post_id)
    #comments = Comment.query.all()
    return render_template('show_comment.html' , post = post , comments = comments)



@posts.route("/user/<string:username>")
def user_all_post(username):
     page = request.args.get('page', 1, type=int)
     user = User.query.filter_by(username=username).first_or_404()
     posts = Post.query.filter_by(author=user)\
        .order_by(Post.timestamp.desc())\
        .paginate(page=page, per_page=2)
     return render_template('user_posts.html' , user = user, posts=posts)
