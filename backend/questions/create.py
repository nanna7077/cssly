import datetime
import random
from flask import Blueprint, request, jsonify

from auth import *
from common import *

questions_create = Blueprint("questions_create", __name__)

@questions_create.route("/challenges/<int:challengeID>/view/questions/<int:questionID>/save", methods=["POST"])
@auth.login_required
def questions_save_solution(challengeID, questionID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        requestData = request.get_json(force=True)

        code = requestData.get("code")
        if not code:
            return {"error": "Code cannot be empty"}, 400
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeUserEnrollment:
            return {"error": "Not enrolled to challenge "}, 400
        if challenge.startTime > datetime.datetime.now():
            return {"error": "Challenge has Not started"}, 400
        if challenge.isClosed or challenge.endTime < datetime.datetime.now():
            return {"error": "Challenge Ended"}, 400
        
        challengeUserSolution = ChallengeUserSolution.query.filter_by(challengeID=challengeID, userID=requestUser.id, challengeQuestionID=questionID).first()
        if not challengeUserSolution:
            return {"error": "Question not found"}, 404
        challengeUserSolution.code = code
        challengeUserSolution.lastUpdatedOn = datetime.datetime.now()
        db.session.commit()

        return {"message": "Saved Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_save_solution")

@questions_create.route("/challenges/<int:challengeID>/save/copypaste", methods=["POST"])
@auth.login_required
def questions_save_copypaste(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeUserEnrollment:
            return {"error": "Not enrolled to challenge "}, 400
        if challenge.startTime > datetime.datetime.now():
            return {"error": "Challenge has Not started"}, 400
        if challenge.isClosed or challenge.endTime < datetime.datetime.now():
            return {"error": "Challenge Ended"}, 400
        
        challengeUserEnrollment.copyPasteCount += 1

        db.session.commit()

        return {"message": "Saved Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_save_copypaste")

@questions_create.route("/challenges/<int:challengeID>/save/tabswitch", methods=["POST"])
@auth.login_required
def questions_save_tabswitch(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeUserEnrollment:
            return {"error": "Not enrolled to challenge "}, 400
        if challenge.startTime > datetime.datetime.now():
            return {"error": "Challenge has Not started"}, 400
        if challenge.isClosed or challenge.endTime < datetime.datetime.now():
            return {"error": "Challenge Ended"}, 400
        
        challengeUserEnrollment.tabSwitchCount += 1

        db.session.commit()

        return {"message": "Saved Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_save_tabswitch")

@questions_create.route("/challenges/<int:challengeID>/save/enrollments/<int:userID>/solutions/<int:questionID>", methods=["POST"])
@auth.login_required
def questions_save_individual_user_responses_eval(challengeID, userID, questionID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        requestData = request.get_json(force=True)
        
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        challengeAdmin = ChallengeAdmin.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeAdmin:
            if not Challenge.query.filter_by(id=challengeID, creatorID=requestUser.id).first():
                return {"error": "You are not an admin of this challenge"}, 400
        challengeSolution = ChallengeUserSolution.query.filter_by(challengeID=challengeID, userID=userID, challengeQuestionID=questionID).first()
        if not challengeSolution:
            return {"error": "Solution not found"}, 404
        
        correctness = requestData['correctness']
        challengeSolution.correctness = correctness
        challengeSolution.evaluationOn = datetime.datetime.now()
        challengeSolution.evaluationBy = requestUser.id
        db.session.commit()

        return {"message": "Saved Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_save_individual_user_responses_eval")