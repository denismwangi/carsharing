import logging
from .routes.cars import cars
from .routes.users import users
from .utils.responses import response_with
from .utils import responses as resp



@cars.errorhandler(400)
@users.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@cars.errorhandler(403)
@users.errorhandler(403)
def forbidden_access(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_400)


@cars.errorhandler(404)
@users.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)

@cars.errorhandler(500)
@users.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)