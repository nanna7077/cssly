from flask_httpauth import HTTPTokenAuth
from database import *
import constants

auth = HTTPTokenAuth(scheme="Bearer", realm=None, header=constants.AUTHHEADER)


@auth.verify_token
def verify_password(sessionkey):
    if Session.query.filter_by(sessionkey=sessionkey).first() != None:
        return True
    return False


@auth.error_handler
def handle401(error):
    return {"error": "UnAuthorized"}, 401


def getRequestUser(sessionkey):
    requestsession = Session.query.filter_by(sessionkey=sessionkey).first()
    if not requestsession:
        return None
    if not requestsession.user:
        return None
    return requestsession.user
