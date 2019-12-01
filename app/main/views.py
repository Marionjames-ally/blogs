from flask import render_template,request,redirect,url_for
from . import main
from app.request import get_quote

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title ='my blogquote'
    quote=get_quote()
    return render_template('index.html',title=title,quote=quote)