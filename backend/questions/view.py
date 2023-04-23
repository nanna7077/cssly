import datetime
import random
from flask import Blueprint, request, jsonify

from auth import *
from common import *

questions_view = Blueprint("questions_view", __name__)

@questions_view.route("/challenges/<int:challengeID>/view/questions")
@auth.login_required
def questions_view_questions(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        questions = {}
        for question in ChallengeUserSolution.query.filter_by(userID=requestUser.id, challengeID=challengeID).all():
            q = ChallengeQuestion.query.filter_by(id=question.challengeQuestionID).first()
            questions[q.id] = {
                "question": q.question,
                "questionMediaType": q.solutionMediaType,
                "questionFileLink": q.solutionFileLink,
                "code": question.code,
                "lastUpdatedOn": question.lastUpdatedOn.strftime("%d %b %Y %H:%M:%S"),
                "evaluationBy": "System" if question.evaluationBy == -1 else User.query.filter_by(id=question.evaluationBy).first().username,
                "evaluationOn": question.evaluationOn.strftime("%d %b %Y %H:%M:%S") if question.evaluationOn else "Not Evaluated Yet",
                "correctness": question.correctness,
                "isEvaluated": True if question.evaluationOn else False,
                "isManualEvaluation": Challenge.query.filter_by(id=question.challengeID).first().isManualEvaluation,
            }
        
        return {"message": "Success", "questions": questions}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_view_questions")

@questions_view.route("/challenges/<int:challengeID>/view/enrollments/<int:userID>/solutions")
@auth.login_required
def questions_view_individual_user_responses(challengeID, userID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        challengeAdmin = ChallengeAdmin.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeAdmin:
            if not Challenge.query.filter_by(id=challengeID, creatorID=requestUser.id).first():
                return {"error": "You are not an admin of this challenge"}, 400
        
        questions = {}
        for question in ChallengeUserSolution.query.filter_by(userID=userID, challengeID=challengeID).all():
            q = ChallengeQuestion.query.filter_by(id=question.challengeQuestionID).first()
            questions[q.id] = {
                "question": q.question,
                "questionMediaType": q.solutionMediaType,
                "questionFileLink": q.solutionFileLink,
                "code": question.code,
                "lastUpdatedOn": question.lastUpdatedOn.strftime("%d %b %Y %H:%M:%S"),
                "evaluationBy": "System" if question.evaluationBy == -1 else User.query.filter_by(id=question.evaluationBy).first().username,
                "evaluationOn": question.evaluationOn.strftime("%d %b %Y %H:%M:%S") if question.evaluationOn else "Not Evaluated Yet",
                "correctness": question.correctness,
                "isEvaluated": True if question.evaluationOn else False,
                "isManualEvaluation": Challenge.query.filter_by(id=question.challengeID).first().isManualEvaluation,
            }
        
        return {"message": "Success", "questions": questions}, 200

    except Exception as err:
        return handle500Error(err, request, "questions_view_individual_user_responses")