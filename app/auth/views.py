from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .. import db
from ..user import User
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "blog login"
    return render_template('auth/login.html', login_form=login_form, title=title)


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    title = "New Account"
    return render_template('auth/regestration.html', registration_form=form, title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))