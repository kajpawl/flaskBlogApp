from flask import Blueprint, render_template, request, jsonify

error_pages = Blueprint('error_pages', __name__)


@error_pages.app_errorhandler(405)
def error_405(error):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'msg': 'Error: Method Not Allowed'})
        response.status_code = 405
        return response
    return render_template('error_pages/405.html'), 405


@error_pages.app_errorhandler(404)
def error_404(error):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'msg': 'Error: Not Found'})
        response.status_code = 404
        return response
    return render_template('error_pages/404.html'), 404


@error_pages.app_errorhandler(403)
def error_403(error):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'msg': 'Error: Forbidden'})
        response.status_code = 403
        return response
    return render_template('error_pages/403.html'), 403


@error_pages.app_errorhandler(401)
def error_401(error):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'msg': 'Error: Unauthorized'})
        response.status_code = 401
        return response
    return render_template('error_pages/401.html'), 401


@error_pages.app_errorhandler(400)
def error_400(error):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'msg': 'Error: Bad Request'})
        response.status_code = 400
        return response
    return render_template('error_pages/400.html'), 400
