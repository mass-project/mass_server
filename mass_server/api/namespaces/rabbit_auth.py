from flask import jsonify
from flask import current_app as app
from flask_slimrest.decorators import add_endpoint
from flask_modular_auth import privilege_required, AuthenticatedPrivilege

from mass_server.api.config import api


@api.add_namespace('/rabbit')
class RabbitAuth:
    @add_endpoint('/auth/user/')
    def user(self):
        return "allow"

    @add_endpoint('/auth/vhost/')
    def vhost(self):
        return "allow"

    @add_endpoint('/auth/resource/')
    def resource(self):
        return "allow"

    @add_endpoint('/auth/topic/')
    def topic(self):
        return "allow"

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/stomp_queue/')
    def element_queue(self):
        # TODO: Replace dummy implementation
        info = {
            'user': 'guest',
            'password': 'guest',
            'websocket': app.config['WEBSTOMP_URL']
        }

        return jsonify(info), 200

