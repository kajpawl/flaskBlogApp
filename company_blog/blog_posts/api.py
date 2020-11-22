from flask import request, Blueprint, abort, jsonify
from company_blog import db
from company_blog.models import BlogPost

blog_posts_api = Blueprint('blog_posts_api', __name__)


@blog_posts_api.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@blog_posts_api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify(post.to_json())


@blog_posts_api.route('/posts', methods=['POST'])
# @login_required
def create_post():
    user_id = 1  # TODO: replace with current_user
    post = BlogPost.from_json(request.json, user_id)

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json()), 201


@blog_posts_api.route('/posts/<int:post_id>', methods=['PUT', 'PATCH'])
# @login_required
def update_post(post_id):
    user_id = 1  # TODO: replace with current_user
    post = BlogPost.query.get_or_404(post_id)

    if post.author.id != user_id:
        abort(403)

    post.text = request.json.get('text', post.text)
    post.title = request.json.get('title', post.title)

    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json())


@blog_posts_api.route('posts/<int:post_id>', methods=['DELETE'])
# @login_required
def delete_post(post_id):
    user_id = 1  # TODO: replace with current_user
    post = BlogPost.query.get_or_404(post_id)

    if post.user_id != user_id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': f'Post {post_id} deleted.'})
