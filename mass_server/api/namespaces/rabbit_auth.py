from flask_slimrest.decorators import add_endpoint

from mass_server.api.config import api


@api.add_namespace('/rabbit/auth')
class RabbitAuth:
    @add_endpoint('/user/')
    def user(self):
        return "allow"

    @add_endpoint('/vhost/')
    def vhost(self):
        return "allow"

    @add_endpoint('/resource/')
    def resource(self):
        return "allow"

    @add_endpoint('/topic/')
    def topic(self):
        return "allow"
