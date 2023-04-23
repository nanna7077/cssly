import json
import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from dotenv import load_dotenv

from common import *
from database import *

from useractions import create as useractions_create
from useractions import view as useractions_view
from challenges import create as challenges_create
from challenges import view as challenges_view
from questions import create as questions_create
from questions import view as questions_view

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(40)
app.config["MAX_CONTENT_LENGTH"] = 7 * 1024 * 1024  # 7 => MB


uri = os.getenv("DATABASE_URL")
if not uri:
    print("[ERROR] Database URI Not Specified")
    exit()
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

from auth import *

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def root():
    try:
        return jsonify({"message": "Hello World"}), 200
    except Exception as err:
        return handle500Error(err, request)

@app.route("/is-logged-in")
@auth.login_required
def is_logged_required():
    try:
        user = getRequestUser(request.headers.get(constants.AUTHHEADER))
        userinf={
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "created_on": user.created_on,
            "isAdmin": user.admin
        }
        return (
            jsonify(
                {
                    "message": "Logged In",
                    "user": userinf,
                }
            ),
            200,
        )
    except Exception as err:
        return handle500Error(err, request, "is-logged-in")


@app.errorhandler(HTTPException)
def handleOtherErrors(error):
    handle500Error(
        f"{error.name}",
        request.url,
        f"{error.description}",
    )
    response = error.get_response()
    response.data = json.dumps({"error": error.description})
    response.content_type = "application/json"
    return response

@app.errorhandler(HTTPException)
def handleOtherErrors(error):
    handle500Error(f'{error.name}', request, f'{error.description}')
    response=error.get_response()
    response.data=json.dumps({'error': error.description})
    response.content_type="application/json"
    return response

app.register_blueprint(useractions_create.useractions_create)
app.register_blueprint(useractions_view.useractions_view)
app.register_blueprint(challenges_create.challenges_create)
app.register_blueprint(challenges_view.challenges_view)
app.register_blueprint(questions_create.questions_create)
app.register_blueprint(questions_view.questions_view)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=os.getenv("PORT", 5000), debug=False, use_reloader=True
    )
