from flask import abort, redirect, render_template, request, url_for,abort,flash
from flask_login import current_user, login_required, login_user, logout_user, login_manager

from app.request import get_quote

from .. import db
from ..user import Blog, Comment, User
from . import main
from .forms import BlogForm, CommentForm, UpdateProfile,UpForm




@main.route('/', methods=['GET', 'POST'])
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'my blogquote'
    quote = get_quote()
    blogs = Blog.query.all()
    return render_template('index.html', title=title, quote=quote, blogs=blogs)


@main.route('/blog/new', methods=['GET', 'POST'])
@login_required
def blogs():
    """
    view blog function to create a new blog
    """
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        title = blog_form.title.data
        content = blog_form.content.data
        print(current_user._get_current_object().id)
        blog = Blog(user_id=current_user._get_current_object().id,
                    title=title, content=content)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('new_blog.html',  blog_form=blog_form)


@main.route('/delete/blog,<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    if blog is not None:
        blog.delete_blog()
  
    return redirect(url_for('main.index',))

@main.route("/blog/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_blog(id):
    blog = Blog.query.filter_by(id = id).first()
    if blog is None:
        abort(404)
    form = UpForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        print(current_user._get_current_object().id)
        blog = Blog(user_id=current_user._get_current_object().id,
                title=title, content=content)
        
        db.session.add(blog)
        db.session.commit()
    
        return redirect(url_for('main.index', blog_id=blog.id))
    elif request.method == 'GET':
        title = form.title.data
        content = form.content.data
    return render_template('blog.html',form=form)


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/comment/new/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog = Blog.query.get(blog_id)
    if form.validate_on_submit():
        content = form.content.data

        new_comment = Comment(
            content=content, user_id=current_user._get_current_object().id, blog_id=blog_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', blog_id=blog_id))

    comments = Comment.query.filter_by(blog_id=blog_id).all()
    print(comments)
    return render_template('comments.html', form=form, blog=blog, comments=comments)


@main.route('/delete/new/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    form = CommentForm()
    if comment is not None:
        comment.delete_comment()
        return redirect(url_for('main.index'))

    return render_template('comments.html', form=form)