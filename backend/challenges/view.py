from hashlib import sha256
from flask import Blueprint, request, jsonify

from auth import *
from common import *

challenges_view = Blueprint("challenges_view", __name__)

@challenges_view.route("/challenges/view/all")
@auth.login_required
def challenges_view_all():
    try:

        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        globalChallenges = {}
        challenges = Challenge.query.filter(Challenge.endTime > datetime.datetime.now(), Challenge.inviteOnly == False, Challenge.isClosed == False, Challenge.creatorID == requestUser.id).all()
        challenges += Challenge.query.filter(Challenge.endTime > datetime.datetime.now(), Challenge.inviteOnly == False, Challenge.isClosed == False, Challenge.creatorID != requestUser.id).all()
        
        enrolledChallenges = ChallengeUserEnrollment.query.filter_by(userID=requestUser.id).all()
        for enrolledChallenge in enrolledChallenges:
            try:
                idx = [c.id for c in challenges].index(enrolledChallenge.id)
                challenges.pop(idx)
            except:
                pass

        for challenge in challenges:
            globalChallenges[challenge.id] = {
                "name": challenge.name,
                "description": challenge.description,
                "createdOn": challenge.created_on.strftime("%d %b %Y %H:%M:%S"),
                "creator": User.query.filter_by(id=challenge.creatorID).first().username,
                "startTime": challenge.startTime.strftime("%d %b %Y %H:%M:%S") if challenge.startTime != None else None,
                "endTime": challenge.endTime.strftime("%d %b %Y %H:%M:%S") if challenge.endTime != None else None,
                "questionPoolSize": len(ChallengeQuestion.query.filter_by(challengeID=challenge.id).all()),
                "numberOfQuestions": challenge.numberOfQuestions,
            }
        
        return {"message": "Success", "challenges": globalChallenges}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_all")

@challenges_view.route("/challenges/view/<int:challengeID>/leaderboard")
@auth.login_required
def challenges_view_leaderboard(challengeID):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401

        challenge = Challenge.query.filter_by(id=challengeID).first()
        
        isAdmin = False
        if challenge.creatorID == requestUser.id:
            isAdmin = True
        if ChallengeAdmin.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first():
            isAdmin = True
        
        if (not isAdmin and not challenge.showLeaderBoardToAll):
            return {"error": "You are not authorized to view this leaderboard"}, 401
        
        leaderboard_ = []
        challengeUserEnrollments = ChallengeUserEnrollment.query.filter_by(challengeID=challengeID).all()
        for challengeUserEnrollment in challengeUserEnrollments:
            score = 0
            for q in ChallengeUserSolution.query.filter_by(challengeID=challengeID, userID=challengeUserEnrollment.userID).all():
                score += q.correctness
            leaderboard_.append(
                {
                    "username": User.query.filter_by(id=challengeUserEnrollment.userID).first().username,
                    "score": score,
                }
            )
        sorted(leaderboard_, key=lambda k: k['score'], reverse=True)

        leaderboard = {}
        rank = 1
        for i in range(len(leaderboard_)):
            leaderboard[rank] = {
                "username": leaderboard_[i]["username"],
                "score": leaderboard_[i]["score"],
            }
            rank += 1
        
        return {"message": "Success", "leaderboard": leaderboard}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_leaderboard")


@challenges_view.route("/challenges/view/global/leaderboard")
@auth.login_required
def challenges_view_gloablLeaderboard():
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        leaderboard_ = {}
        challengeUserEnrollments = ChallengeUserEnrollment.query.all()
        for challengeUserEnrollment in challengeUserEnrollments:
            score = 0
            for q in ChallengeUserSolution.query.filter_by(userID=challengeUserEnrollment.userID).all():
                score += q.correctness
            leaderboard_[User.query.filter_by(id=challengeUserEnrollment.userID).first().username] = score
        leaderboard_ = dict(sorted(leaderboard_.items(), key=lambda x: x[1], reverse=True))

        leaderboard = {}
        rank = 1
        for k in leaderboard_.keys():
            leaderboard[rank] = {
                "username": k,
                "score": leaderboard_[k],
            }
            rank += 1
        
        return {"message": "Success", "leaderboard": leaderboard}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_gloablLeaderboard")

@challenges_view.route("/challenges/view/enrolled")
@auth.login_required
def challenges_view_enrolled():
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        challenges = {}
        challenges_ = []
        challengeUserEnrollments = ChallengeUserEnrollment.query.filter_by(userID=requestUser.id).all()
        for challengeUserEnrollment in challengeUserEnrollments:
            challenges_.append(Challenge.query.filter_by(id=challengeUserEnrollment.challengeID).first())
        for challenge in challenges_:
            challenges[challenge.id] = {
                "name": challenge.name,
                "description": challenge.description,
                "createdOn": challenge.created_on.strftime("%d %b %Y %H:%M:%S"),
                "creator": User.query.filter_by(id=challenge.creatorID).first().username,
                "startTime": challenge.startTime.strftime("%d %b %Y %H:%M:%S") if challenge.startTime != None else None,
                "endTime": challenge.endTime.strftime("%d %b %Y %H:%M:%S") if challenge.endTime != None else None,
                "questionPoolSize": len(ChallengeQuestion.query.filter_by(challengeID=challenge.id).all()),
                "numberOfQuestions": challenge.numberOfQuestions,
            }
        
        return {"message": "Success", "challenges": challenges}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_enrolled")

@challenges_view.route("/challenges/view/administering")
@auth.login_required
def challenges_view_administering():
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        challenges = {}
        challenges_ = []
        for challenge in Challenge.query.filter_by(creatorID=requestUser.id).all():
            challenges_.append(challenge)
        for ca in ChallengeAdmin.query.filter_by(userID=requestUser.id).all():
            challenges_.append(Challenge.query.filter_by(id=ca.challengeID).first())
        for challenge in challenges_:
            challenges[challenge.id] = {
                "name": challenge.name,
                "description": challenge.description,
                "createdOn": challenge.created_on.strftime("%d %b %Y %H:%M:%S"),
                "creator": User.query.filter_by(id=challenge.creatorID).first().username,
                "startTime": challenge.startTime.strftime("%d %b %Y %H:%M:%S") if challenge.startTime != None else None,
                "endTime": challenge.endTime.strftime("%d %b %Y %H:%M:%S") if challenge.endTime != None else None,
                "questionPoolSize": len(ChallengeQuestion.query.filter_by(challengeID=challenge.id).all()),
                "numberOfQuestions": challenge.numberOfQuestions,
            }
        
        return {"message": "Success", "challenges": challenges}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_administering")

@challenges_view.route("/challenges/view/<int:id>")
@auth.login_required
def challenges_view_individual(id):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        challenge = Challenge.query.filter_by(id=id).first()
        if not challenge:
            return {"error": "Challenge does not exist"}, 400
        challengeUserEnrollment = ChallengeUserEnrollment.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first()

        isAdmin = False
        if challenge.creatorID == requestUser.id:
            isAdmin = True
        if ChallengeAdmin.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first():
            isAdmin = True

        challengeret = {
                "name": challenge.name,
                "isAdmin": isAdmin,
                "description": challenge.description,
                "createdOn": challenge.created_on.strftime("%d %b %Y %H:%M:%S"),
                "creator": User.query.filter_by(id=challenge.creatorID).first().username,
                "startTime": challenge.startTime.strftime("%d %b %Y %H:%M:%S") if challenge.startTime != None else None,
                "endTime": challenge.endTime.strftime("%d %b %Y %H:%M:%S") if challenge.endTime != None else None,
                "isTabSwitchingRestricted": challenge.restrictTabSwitching,
                "isCopyPasteRestricted": challenge.restrictCopyPaste,
                "isManuallyEvaluated": challenge.isManualEvaluation,
                "isClosed": challenge.isClosed,
                "ended": challenge.endTime < datetime.datetime.now(),
                "notStarted": challenge.startTime > datetime.datetime.now(),
                "inviteOnly": challenge.inviteOnly,
                "isPublicLeaderboard": challenge.showLeaderBoardToAll,
                "enrolled": True if challengeUserEnrollment else False,
                "enrolledOn": challengeUserEnrollment.created_on.strftime("%d %b %Y %H:%M:%S") if challengeUserEnrollment else '',
                "questionPoolSize": len(ChallengeQuestion.query.filter_by(challengeID=challenge.id).all()),
                "numberOfQuestions": challenge.numberOfQuestions,
        }

        if isAdmin:
            challengeret['currentAdmins'] = [User.query.filter_by(id=c.userID).first().username for c in ChallengeAdmin.query.filter_by(challengeID=challenge.id).all()] + [User.query.filter_by(id=challenge.creatorID).first().username]
        
        return {"message": "Success", "challenge": challengeret}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_individual")

@challenges_view.route("/challenges/view/<int:id>/enrollments/viewall")
@auth.login_required
def challenges_view_allenrollments(id):
    try:
        requestUser = getRequestUser(request.headers.get(constants.AUTHHEADER))
        if requestUser == None:
            return {"error": "Invalid sessionkey"}, 401
        
        challenge = Challenge.query.filter_by(id=id).first()
        if not challenge:
            return {"error": "Challenge does not exist"}, 400

        isAdmin = False
        if challenge.creatorID == requestUser.id:
            isAdmin = True
        if ChallengeAdmin.query.filter_by(challengeID=challenge.id, userID=requestUser.id).first():
            isAdmin = True
        if not isAdmin:
            return {"error": "You are not an admin of this challenge"}, 400

        enrollments = {}
        for enrollment in ChallengeUserEnrollment.query.filter_by(challengeID=challenge.id).all():
            questions = ChallengeUserSolution.query.filter_by(userID=enrollment.userID, challengeID=challenge.id).all()
            isNotEvaluated = True
            for question in questions:
                if question.evaluationOn != None:
                    isNotEvaluated = False
                    break
            enrollments[enrollment.id] = {
                "userID": enrollment.userID,
                "username": User.query.filter_by(id=enrollment.userID).first().username,
                "tabSwitchCount": enrollment.tabSwitchCount,
                "copyPasteCount": enrollment.copyPasteCount,
                "startedOn": enrollment.startedOn.strftime("%d %b %Y %H:%M:%S") if enrollment.startedOn != None else None,
                "createdOn": enrollment.created_on.strftime("%d %b %Y %H:%M:%S"),
                "isNotEvaluated": isNotEvaluated
            }
        
        return {"message": "Success", "enrollments": enrollments}, 200

    except Exception as err:
        return handle500Error(err, request, "challenges_view_allenrollments")
