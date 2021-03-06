from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from company_blog import db
from company_blog.models import User, BlogPost
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from company_blog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        incorrect_user_data = False
        user_with_email = User.query.filter_by(email=form.email.data).first()
        user_with_username = User.query.filter_by(username=form.username.data).first()
        if user_with_email:
            incorrect_user_data = True
            form.email.errors = ['This email is already used.']
        if user_with_username:
            incorrect_user_data = True
            form.username.errors = ['This username is already used.']
        if not incorrect_user_data:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()

            flash('Thank you for registering!', 'success')
            return redirect(url_for('users.login'))

    if request.method == 'POST':
        flash('Please correct all errors.', 'danger')

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Login success!', 'success')

            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    if request.method == 'POST':
        flash('Incorrect email or password.', 'danger')

    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'warning')
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        incorrect_user_data = False
        user_with_email = User.query.filter_by(email=form.email.data).first()
        user_with_username = User.query.filter_by(username=form.username.data).first()
        if user_with_email and user_with_email != current_user:
            incorrect_user_data = True
            form.email.errors = ['This email is already used.']
        if user_with_username and user_with_username != current_user:
            incorrect_user_data = True
            form.username.errors = ['This username is already used.']
        if incorrect_user_data:
            profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
            flash('Please correct all errors.', 'danger')
            return render_template('account.html', profile_image=profile_image, form=form)

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('User account updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
