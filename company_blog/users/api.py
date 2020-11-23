from flask import request, Blueprint, abort, jsonify
from company_blog import db
from company_blog.models import User, BlogPost

users_api = Blueprint('users_api', __name__)


@users_api.route('/users/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if not email or not username or not password:
        abort(403)

    user_with_email = User.query.filter_by(email=email).first()
    user_with_username = User.query.filter_by(username=username).first()
    if user_with_email or user_with_username:
        abort(403)

    new_user = User(email=email,
                    username=username,
                    password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json(new_user.id)), 201


@users_api.route('/users/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first_or_404()
    if not user.check_password(password):
        abort(403)
    # TODO: actually login user
    return jsonify(user.to_json(user.id))


@users_api.route('/users/logout')
def logout():
    # TODO: logout user
    return jsonify({'message': 'User logged out.'})


@users_api.route('/users/account', methods=['GET'])
# @login_required
def account():
    user_id = 1  # TODO: replace with current_user
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json(user_id))


@users_api.route('/users', methods=['GET'])
# @login_required
def get_users():
    users_list = User.query.all()
    return jsonify({'users': [user.to_json() for user in users_list]})


@users_api.route('/users/<username>', methods=['GET'])
# @login_required
def get_user(username):
    user_id = 1  # TODO: replace with current_user
    user = User.query.filter_by(username=username).first_or_404()
    return jsonify(user.to_json(user_id))


@users_api.route('/users/<username>', methods=['PUT', 'PATCH'])
# @login_required
def update_user(username):
    user_id = 1  # TODO: replace with current_user
    user = User.query.filter_by(username=username).first_or_404()
    confirm_password = user.check_password(request.json.get('confirm_password'))
    if not confirm_password or user.id != user_id:
        abort(403)

    user_with_email = User.query.filter_by(email=request.json.get('email')).first()
    user_with_username = User.query.filter_by(username=request.json.get('username')).first()
    if user_with_email or user_with_username:
        abort(403)

    user.email = request.json.get('email', user.email)
    user.username = request.json.get('username', user.username)
    user.password = request.json.get('password', user.password)

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json(user_id))


@users_api.route('/users/<username>', methods=['DELETE'])
# @login_required
def delete_user(username):
    user_id = 1  # TODO: replace with current_user
    user = User.query.filter_by(username=username).first_or_404()
    if user.id != user_id:
        abort(403)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {username} deleted.'})


@users_api.route('/users/<username>/posts')
# @login_required
def get_user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return jsonify(
        {'total': posts.total, 'pages': posts.pages, 'page': posts.page, 'per_page': posts.per_page,
         'posts': [post.to_json() for post in posts.items]})
