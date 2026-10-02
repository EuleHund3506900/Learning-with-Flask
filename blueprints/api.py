import os

from flask import Blueprint, jsonify, request

from base.jwt import verify_jwt
from blueprints.utils.middleware import require_authentication
from database.db import (
    create_completed,
    create_favorite,
    delete_completed,
    delete_favorite,
    get_completed_by_user,
    get_favorites_by_user,
)
from blueprints.utils.files import count_lectures_in_directory

api_bp = Blueprint('api', __name__, url_prefix='/api')


def _current_user_id():
    payload = verify_jwt(request.cookies.get('token'))
    return payload['user_id']


@api_bp.route('/courses/lectures', methods=['GET'])
def course_lecture_count():
    course_path = request.args.get('course_path', '').strip()
    learning_root = os.path.abspath('local_data/Learning')
    resolved_course_path = os.path.abspath(course_path)

    if not course_path:
        return jsonify({'message': 'course_path is required'}), 400

    try:
        is_course_path = os.path.commonpath([learning_root, resolved_course_path]) == learning_root
    except ValueError:
        is_course_path = False

    if not is_course_path or not os.path.isdir(resolved_course_path):
        return jsonify({'message': 'course was not found'}), 404

    return jsonify({
        'course_path': course_path,
        'total_lectures': count_lectures_in_directory(resolved_course_path),
    })


@api_bp.route('/favorites', methods=['GET', 'POST'])
@require_authentication
def favorites():
    user_id = _current_user_id()

    if request.method == 'GET':
        return jsonify({'favorites': get_favorites_by_user(user_id)})

    data = request.get_json(silent=True)
    item_url = data.get('item_url', '').strip() if isinstance(data, dict) else ''
    if not item_url:
        return jsonify({'message': 'item_url is required'}), 400

    if data.get('favorite') is False:
        delete_favorite(user_id, item_url)
        return jsonify({'favorite': {'item_url': item_url}, 'active': False})

    favorite, created = create_favorite(user_id, item_url)
    return jsonify({'favorite': favorite}), 201 if created else 200


@api_bp.route('/completed', methods=['GET', 'POST'])
@require_authentication
def completed():
    user_id = _current_user_id()

    if request.method == 'GET':
        return jsonify({'completed': get_completed_by_user(user_id)})

    data = request.get_json(silent=True)
    item_url = data.get('item_url', '').strip() if isinstance(data, dict) else ''
    if not item_url:
        return jsonify({'message': 'item_url is required'}), 400

    if data.get('completed') is False:
        delete_completed(user_id, item_url)
        return jsonify({'completed': {'item_url': item_url}, 'active': False})

    completed_item, created = create_completed(user_id, item_url)
    return jsonify({'completed': completed_item}), 201 if created else 200
