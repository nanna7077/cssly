import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    creatorID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    startTime = db.Column(db.DateTime, nullable=True)
    endTime = db.Column(db.DateTime, nullable=True)
    isClosed = db.Column(db.Boolean, nullable=False, default=False)
    numberOfQuestions = db.Column(db.Integer, nullable=False, default=3)
    showLeaderBoardToAll = db.Column(db.Boolean, nullable=True)
    inviteOnly = db.Column(db.Boolean, nullable=False)
    restrictTabSwitching = db.Column(db.Boolean, nullable=False)
    restrictCopyPaste = db.Column(db.Boolean, nullable=False)
    isManualEvaluation = db.Column(db.Boolean, nullable=False, default=False)


class ChallengeAdmin(db.Model):
    __tablename__ = 'challenge_admins'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challengeID = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    addedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    addedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ChallengeQuestion(db.Model):
    __tablename__ = 'challenge_questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1024), unique=False, nullable=False)
    solutionMediaType = db.Column(db.Integer, nullable=False, default=0) # 0 - Image, 1 - Video
    solutionFileLink = db.Column(db.String(80), unique=False, nullable=False) # name of the file that contains the solution - image file.
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challengeID = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)


class ChallengeUserEnrollment(db.Model):
    __tablename__ = 'challenge_user_enrollment'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challengeID = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    tabSwitchCount = db.Column(db.Integer, nullable=False, default=0)
    copyPasteCount = db.Column(db.Integer, nullable=False, default=0)
    startedOn = db.Column(db.DateTime, nullable=True, default=None)

    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ChallengeUserSolution(db.Model):
    __tablename__ = 'challenge_user_solutions'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challengeID = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    challengeQuestionID = db.Column(db.Integer, db.ForeignKey('challenge_questions.id'), nullable=False)
    code = db.Column(db.String(16000), nullable=False, default="""
<!DOCTYPE html>
<html>
    <body>
        <style>
            div {
                width: 100px;
                height: 100px;
                background: #ff00bb;
            }
        </style>
        <div></div>
    </body>
</html>
""")
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    lastUpdatedOn = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    correctness = db.Column(db.Float, nullable=False, default=0.0)
    evaluationBy = db.Column(db.Integer, nullable=False, default=-1) # -1 means System
    evaluationOn = db.Column(db.DateTime, nullable=True, default=None)

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sessionkey = db.Column(db.String(120), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref=db.backref('sessions', lazy=True))