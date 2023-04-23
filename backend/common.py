import os

import datetime
import random
import string

import constants
from database import *

def createSession(user):
    random_string = ""
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [8, 4, 4, 4, 12]
    for n in uuid_format:
        for i in range(0, n):
            random_string += str(
                random_str_seq[random.randint(0, len(random_str_seq) - 1)]
            )
        if n != 12:
            random_string += "-"
    session = Session(
        sessionkey=random_string,
        userID=user.id,
        created_on=datetime.datetime.now(),
    )
    db.session.add(session)
    db.session.commit()
    return random_string


def handle500Error(err, request, funcname="Function not identified"):
    uniqueID = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(64)
    )
    with open(os.path.join(constants.LOGFILE_DIRECTORY, f"{datetime.datetime.now().strftime('%d-%m-%Y')}"), 'a') as logfile:
        logfile.write(f"Error ID: {uniqueID} in function {funcname}:\n{repr(err)}\n{request.get_data()}\n{request.__dict__}\n\n")
    return {"error": f"Exception ID: {uniqueID}. Please share this Exception ID with instance owner."}, 500