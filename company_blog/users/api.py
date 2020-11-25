from flask import request, Blueprint, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash
from company_blog import db
from company_blog.models import User, BlogPost

users_api = Blueprint('users_api', __name__)


@users_api.route('/users/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if not email or not username or not password:
        abort(400)

    user_with_email = User.query.filter_by(email=email).first()
    user_with_username = User.query.filter_by(username=username).first()
    if user_with_email or user_with_username:
        abort(400)

    new_user = User(email=email,
                    username=username,
                    password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_json(new_user.id)), 201


@users_api.route('/users/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        abort(401)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@users_api.route('/users/account', methods=['GET'])
@jwt_required
def account():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json(user_id))


@users_api.route('/users', methods=['GET'])
def get_users():
    users_list = User.query.all()
    return jsonify({'users': [user.to_json() for user in users_list]})


@users_api.route('/users/<username>', methods=['GET'])
def get_user(username):
    user_id = get_jwt_identity()
    user = User.query.filter_by(username=username).first_or_404()
    if not user:
        abort(403)
    return jsonify(user.to_json(user_id))


@users_api.route('/users/<username>', methods=['PUT', 'PATCH'])
@jwt_required
def update_user(username):
    user_id = get_jwt_identity()
    user = User.query.filter_by(username=username).first_or_404()
    confirm_password = user.check_password(request.json.get('confirm_password'))
    if not confirm_password or user.id != user_id:
        abort(403)

    user_with_email = User.query.filter_by(email=request.json.get('email')).first()
    user_with_username = User.query.filter_by(username=request.json.get('username')).first()
    if user_with_email and user_with_email.id != user_id or \
            user_with_username and user_with_username.id != user_id:
        abort(403)

    user.email = request.json.get('email', user.email)
    user.username = request.json.get('username', user.username)
    new_password = request.json.get('password', None)
    if new_password:
        user.password_hash = generate_password_hash(new_password)

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json(user_id))


@users_api.route('/users/<username>', methods=['DELETE'])
@jwt_required
def delete_user(username):
    user_id = get_jwt_identity()
    user = User.query.filter_by(username=username).first_or_404()
    if user.id != user_id:
        abort(403)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': f'User {username} deleted.'})


@users_api.route('/users/<username>/posts')
def get_user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return jsonify(
        {'total': posts.total, 'pages': posts.pages, 'page': posts.page, 'per_page': posts.per_page,
         'posts': [post.to_json() for post in posts.items]})
