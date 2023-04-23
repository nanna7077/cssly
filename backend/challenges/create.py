import datetime
import random
from flask import Blueprint, request, jsonify

from auth import *
from common import *

challenges_create = Blueprint("challenges_create", __name__)

@challenges_create.route("/challenges/create", methods=["POST"])
@auth.login_required
def challenges_create_createNew():
    try:
        requestData = request.get_json(force=True)
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))

        name = requestData.get("name")
        description = requestData.get("description")
        startDate = requestData.get("startDate")
        startTime = requestData.get("startTime")
        endDate = requestData.get("endDate")
        endTime = requestData.get("endTime")
        privateLeaderboard = requestData.get("privateLeaderboard")
        inviteOnly = requestData.get("inviteOnly")
        questionCount = requestData.get("questionCount")
        restrictTabSwitching = requestData.get("restrictTabSwitching")
        restrictCopyPaste = requestData.get("restrictCopyPaste")
        isManualEvaluation = requestData.get("isManualEvaluation")
        questions = requestData.get("questions")

        if None in [name, description, startDate, startTime, endDate, endTime, privateLeaderboard, inviteOnly, restrictTabSwitching, restrictCopyPaste, isManualEvaluation, questions, questionCount]:
            return {"error": "Missing required fields"}, 400
        name, description, startDate, startTime, endDate, endTime, privateLeaderboard, inviteOnly, restrictTabSwitching, restrictCopyPaste, isManualEvaluation, questionCount = str(name), str(description), str(startDate), str(startTime), str(endDate), str(endTime), bool(privateLeaderboard), bool(inviteOnly), bool(restrictTabSwitching), bool(restrictCopyPaste), bool(isManualEvaluation), int(questionCount)
        if len(name.strip()) == 0 or len(description.strip()) == 0 or len(startDate.strip()) == 0 or len(startTime.strip()) == 0 or len(endDate.strip()) == 0 or len(endTime.strip()) == 0 or questionCount <= 0:
            return {"error": "Name/Description/Start Date/Start Time/End Date/End Time cannot be empty"}, 400
        if len(questions) == 0 and type(questions)!=list:
            return {"error": "Questions cannot be empty"}, 400
        if len(questions) < questionCount:
            return {"error": "Questions cannot be less than Participant Shown Questions"}, 400
        
        startDateTime = datetime.datetime.strptime(startDate + " " + startTime, "%Y-%m-%d %H:%M")
        endDateTime = datetime.datetime.strptime(endDate + " " + endTime, "%Y-%m-%d %H:%M")
        if startDateTime >= endDateTime:
            return {"error": "Start Date/Time cannot be greater than or equal to End Date/Time"}, 400
        if (endDateTime - startDateTime) < datetime.timedelta(minutes=30):
            return {"error": "Challenge duration cannot be less than 30 minutes"}, 400
        
        challenge = Challenge(name=name, description=description, startTime=startDateTime, endTime=endDateTime, showLeaderBoardToAll= not privateLeaderboard, inviteOnly=inviteOnly, restrictTabSwitching=restrictTabSwitching, restrictCopyPaste=restrictCopyPaste, isManualEvaluation=isManualEvaluation, creatorID=requestUser.id, numberOfQuestions=questionCount)
        db.session.add(challenge)
        db.session.commit()

        for question in questions:
            newChallengeQuestion = ChallengeQuestion(
                question = question.get("questionDesc"),
                challengeID = challenge.id,
                solutionFileLink = question.get("questionMediaLink"),
                added_by = requestUser.id,
                solutionMediaType = constants.QUESTION_MEDIATYPE_MAPPING[question.get("questionMediaType")],
            )
            db.session.add(newChallengeQuestion)
            db.session.commit()

        return {"message": "Challenge Created Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_createNew")

@challenges_create.route("/challenges/<int:challengeID>/enroll", methods=["POST"])
@auth.login_required
def challenges_create_enroll(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.inviteOnly:
            return {"error": "Challenge is invite only"}, 400
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if challengeUserEnrollment:
            return {"error": "Already enrolled"}, 400
        
        challengeUserEnrollment = ChallengeUserEnrollment(
            userID = requestUser.id,
            challengeID = challengeID
        )
        db.session.add(challengeUserEnrollment)
        db.session.commit()

        return {"message": "Enrolled Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_enroll")

@challenges_create.route("/challenges/<int:challengeID>/addadmin", methods=["POST"])
@auth.login_required
def challenges_create_addadmin(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        requestData = request.get_json(force=True)
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.creatorID != requestUser.id and ChallengeAdmin.query.filter_by(challengeID=challengeID, userID=requestUser.id).first() is None:
            return {"error": "Not authorized"}, 401
        
        adminToAdd = requestData.get("adminToAdd")
        if not adminToAdd:
            return {"error": "Missing required fields"}, 400
        adminToAdd = str(adminToAdd)
        if len(adminToAdd.strip()) == 0:
            return {"error": "Admin to add cannot be empty"}, 400
        adminToAddUser = User.query.filter_by(username=adminToAdd).first()
        if not adminToAddUser:
            return {"error": "User not found"}, 404
        if challenge.creatorID == adminToAddUser.id or ChallengeAdmin.query.filter_by(challengeID=challengeID, userID=adminToAddUser.id).first():
            return {"error": "Already admin"}, 400
        
        challengeAdmin = ChallengeAdmin(
            userID = adminToAddUser.id,
            challengeID = challengeID,
            addedBy = requestUser.id
        )
        db.session.add(challengeAdmin)
        db.session.commit()

        return {"message": "Admin added Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_addadmin")

@challenges_create.route("/challenges/<int:challengeID>/start", methods=["POST"])
@auth.login_required
def challenges_create_start(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID, userID=requestUser.id).first()
        if not challengeUserEnrollment:
            return {"error": "Not enrolled"}, 400
        if challengeUserEnrollment.startedOn:
            return {"message": "Continue."}, 200
        
        challengeUserEnrollment.startedOn = datetime.datetime.now()
        db.session.commit()

        tmp_ = challenge.numberOfQuestions
        questions_ = ChallengeQuestion.query.filter_by(challengeID=challengeID).all()
        while tmp_ > 0:
            q = questions_.pop(random.randint(0, len(questions_)-1))

            challengeUserSolution = ChallengeUserSolution(
                challengeID = challengeID,
                userID = requestUser.id,
                challengeQuestionID = q.id
            )
            db.session.add(challengeUserSolution)
            db.session.commit()

            tmp_ -= 1
        
        return {"message": "Enrolled Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_start")

@challenges_create.route("/challenges/<int:challengeID>/close", methods=["POST"])
@auth.login_required
def challenges_create_close(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        
        isAdmin = False
        if challenge.creatorID == requestUser.id:
            isAdmin = True
        if ChallengeAdmin.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first():
            isAdmin = True
        
        if not isAdmin:
            return {"error": "You are not authorized to view this."}, 401
        
        challenge.isClosed = True
        db.session.commit()

        return {"message": "Challenge closed Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_close")


@challenges_create.route("/challenges/<int:challengeID>/open", methods=["POST"])
@auth.login_required
def challenges_create_open(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        
        challenge = Challenge.query.filter_by(id=challengeID).first()
        if not challenge:
            return {"error": "Challenge not found"}, 404
        if challenge.isClosed:
            return {"error": "Challenge is closed"}, 400
        
        isAdmin = False
        if challenge.creatorID == requestUser.id:
            isAdmin = True
        if ChallengeAdmin.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first():
            isAdmin = True
        
        if not isAdmin:
            return {"error": "You are not authorized to view this."}, 401
        
        challenge.isClosed = False
        db.session.commit()

        return {"message": "Challenge openend Successfully."}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_create_open")