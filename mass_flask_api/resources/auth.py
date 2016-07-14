# from flask import request, jsonify
# from mass_flask_api.config import api_blueprint
# from mass_flask_core.models import User, UserAPIKey
#
#
# def request_auth_token():
#     """
#         ---
#         post:
#             description: Request an auth token for the given user credentials.
#             parameters:
#                 - in: body
#                   name: body
#                   type: string
#             responses:
#                 200:
#                     description: The auth token is returned.
#                 400:
#                     description: Invalid credentials given or the request is malformed.
#         """
#     json_data = request.get_json()
#     if not json_data:
#         return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
#     else:
#         username = json_data.get('username')
#         password = json_data.get('password')
#         user = User.objects(username=username).first()
#         if not user:
#             u = User(username=username, password=password)
#             u.save()
#             return jsonify({'error': 'Invalid credentials.'}), 400
#         else:
#             api_key = UserAPIKey.get_or_create(user)
#             return jsonify({'api_key': api_key.generate_auth_token()}), 200
#
# api_blueprint.add_url_rule('/auth/request_auth_token/', view_func=request_auth_token, methods=['POST'])
# api_blueprint.apispec.add_path(path='/auth/request_auth_token/', view=request_auth_token)
