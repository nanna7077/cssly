var lastQuestionIndex = 0;

function addQuestion() {
    lastQuestionIndex += 1;
    var newdiv = document.createElement('div');
    newdiv.innerHTML = `
    <div style="border: #ff00bb solid 1px; padding: 8px; border-radius: 4px; width: fit-content;" id="question`+lastQuestionIndex+`">
        Question <span style="color: #ff00bb; font-weight: bold;">#`+lastQuestionIndex+`</span>
        <br><br>
        Question <span style="color: #ff00bb;">Description</span><br>
        <textarea id="questiondesc`+lastQuestionIndex+`" maxlength="1024" style="background: none;
        border: none;
        background-color: rgba(255, 255, 255, 0.4);
        color: aliceblue;
        font-size: 1.15rem;
        padding: 4px;
        padding-left: 8px;
        padding-right: 8px;
        margin-top: 4px;
        margin-bottom: 4px;
        width: 95%;" cols="30" rows="3"></textarea>
        <br><br>
        Solution <span style="color: #ff00bb;">Media Type</span>
        <br>
        Image <input type="radio" id="questionmediatypeImage" name="questionmediatype`+lastQuestionIndex+`">
        Video <input type="radio" id="questionmediatypeVideo" name="questionmediatype`+lastQuestionIndex+`">
        <br><br>
        Solution <span style="color: #ff00bb;">Link</span> (Direct Media Link to the Image or Video)
        <br>
        <input type="text" id="questionmedialink`+lastQuestionIndex+`">
        <br><br>
        <button style="font-size: 1rem; background-color: red; color: black;" onclick="removeQuestion(`+lastQuestionIndex+`);">
            - Remove Question
        </button>
    </div>
    `;
    document.getElementById('questions').append(newdiv);
}
function removeQuestion(i) {
    document.getElementById("question"+i).remove();
    if (lastQuestionIndex == i) {
        lastQuestionIndex -= 1;
    }
}

function createChallenge() {
    var challengeName = document.getElementById("challenge-name").value;
    var challengeDescription = document.getElementById("challenge-desc").value;
    var startDate = document.getElementById("challenge-startdate").value;
    var startTime = document.getElementById("challenge-starttime").value;
    var endDate = document.getElementById("challenge-enddate").value;
    var endTime = document.getElementById("challenge-endtime").value;
    var showLeaderboard = document.getElementById("challenge-showleaderboard").checked;
    var inviteOnly = document.getElementById("challenge-inviteonly").checked;
    var restrictTabSwitching = document.getElementById("challenge-restricttabswitch").checked;
    var restrictCopyPaste = document.getElementById("challenge-restrictcopypaste").checked;
    var manualEvaluation = document.getElementById("challenge-manualevaluation").checked;
    var challengeQuestionCount = document.getElementById("challenge-question-count").value;
    var challengeQuestions = [];

    var questionValidation = true;
    [... document.getElementById('questions').children].forEach((e) => {
        var questionDesc = e.querySelector("textarea").value;
        var questionMediaType = e.querySelector("input[type=radio]:checked").id.split("questionmediatype")[1];
        var questionMediaLink = e.querySelector("input[type=text]").value;
        if (questionDesc == "" || questionMediaType == "" || questionMediaLink == "") {
            alert("Please fill in all the fields for questions!");
            questionValidation = false;
            return;
        }
        challengeQuestions.push({
            "questionDesc": questionDesc,
            "questionMediaType": questionMediaType,
            "questionMediaLink": questionMediaLink
        });
    })

    if (!questionValidation) { return; }

    var challengeData = {
        "name": challengeName,
        "description": challengeDescription,
        "questionCount": challengeQuestionCount,
        "startDate": startDate,
        "startTime": startTime,
        "endDate": endDate,
        "endTime": endTime,
        "privateLeaderboard": showLeaderboard,
        "inviteOnly": inviteOnly,
        "restrictTabSwitching": restrictTabSwitching,
        "restrictCopyPaste": restrictCopyPaste,
        "isManualEvaluation": manualEvaluation,
        "questions": challengeQuestions
    }

    fetch(API_URL + '/challenges/create', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': window.localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify(challengeData)
    })
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        window.alert("Challenge Created! You can further manage the challenge from your dashboard.");
        window.location.href = "/pages/home.html";
    })
}

addQuestion();