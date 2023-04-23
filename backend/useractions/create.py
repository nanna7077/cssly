from hashlib import sha256
from flask import Blueprint, request, jsonify

from auth import *
from common import *

useractions_create = Blueprint("useractions_create", __name__)

@useractions_create.route("/users/register", methods=["POST"])
def useractions_create_register():
    try:
        requestData = request.get_json(force=True)

        username = requestData.get("username")
        email = requestData.get("email")
        password = requestData.get("password")

        if None in [username, email, password]:
            return {"error": "Missing required fields"}, 400
        username, email, password = str(username), str(email), str(password)
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
            return {"error": "Username/Email/Password cannot be empty"}, 400

        if User.query.filter_by(username=username).first() != None or User.query.filter_by(email=email).first() != None:
            return {"error": "Username/Email already exists"}, 400
        
        user = User(username=username, email=email, password=sha256(password.encode()).hexdigest())
        db.session.add(user)
        db.session.commit()

        return {"message": "User Created Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "useractions_create_register")


@useractions_create.route("/users/login", methods=["POST"])
def useractions_create_login():
    try:
        requestData = request.get_json(force=True)

        username = requestData.get("username")
        password = requestData.get("password")

        if None in [username, password]:
            return {"error": "Missing required fields"}, 400
        username, password = str(username), str(password)
        if len(username.strip()) == 0 or len(password.strip()) == 0:
            return {"error": "Username/Password cannot be empty"}, 400

        if User.query.filter_by(username=username).first() == None:
            return {"error": "Username doesnot exist"}, 400
        if len(password) == 0:
            return {"error": "Password must not be 0 characters "}, 400
        
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "No such user."}, 404
        if user.password != sha256(password.encode()).hexdigest():
            return {"error": "Incorrect password."}, 401
        sessionkey = createSession(user)
        
        return {"message": "Logged in!", "sessionkey": sessionkey}, 200

    except Exception as err:
        return handle500Error(err, request, "useractions_create_login")


@useractions_create.route("/users/logout", methods=["POST"])
@auth.login_required
def useractions_create_logout():
    try:
        user = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if user == None:
            return {"error": "Invalid Token"}, 400

        Session.query.filter_by(user_id=user.id, sessionkey=request.headers.get(constants.AUTHHEADER)).delete()
        db.session.commit()

        return {"message": "Logged out successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "useractions_create_logout")