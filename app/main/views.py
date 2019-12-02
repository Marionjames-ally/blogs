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

