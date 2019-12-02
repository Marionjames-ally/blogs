from flask import render_template,request,redirect,url_for
from . import main
from app.request import get_quote
from flask_login import current_user, login_required, login_user, logout_user
from .. import db, photos
from ..user import Blog, Comment, User
from . import main
from .forms import BlogForm,commentForm, UpdateProfile, UpForm

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title ='my blogquote'
    quote=get_quote()
    blogs=Blog.querry.all
    return render_template('index.html',title=title,quote=quote,blogs=blogs)


@main.route('/blog/new',methods=['GET','POST'])
@login_required
def blogs():
    '''
    view blog function to create an new blog
    '''
    blog_form=BlogForm()

    if blog_form.validate_on_submit():
        title = blog_form.title.data
        content = blog_form.content.data
        print(current_user._get_current_object().id)
        blog = Blog(user_id=current_user._get_current_object().id,
                    title=title, content=content)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for('main.index'))
        return render_template('new_blog.html', blog_form=blog_form)

@main.route('/delete/blog, <int:id>',methods=['GET','POST'])
@login_required
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    if blog is not None:
        blog.delete_blog()
  
    return redirect(url_for('main.index',))


@main.route('/blog/update, <int:id>',methods=['GET','POST'])
@login_required
def update_blog(id):
    blog=Blog.query.filter_by(id=id).first()
    if blog is None:
        return(404)
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
        return(404)
    return render_template('profile,profile.html', user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        return(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user= User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename= photos.save(request.file['photo'])
        path=f'photos/{filename}'
        user.profile_pic_path = path
        db.session_commit()
        return redirect(url_for('main.profile', uname=uname))
