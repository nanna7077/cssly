var challengeID = null;
var userID = null;

window.location.search.substr(1).split('&').forEach(function (item) {
    var s = item.split('=');
    if (s[0] === 'cid') {
        challengeID = s[1];
    }
    if (s[0] === 'uid') {
        userID = s[1];
    }
})

if (challengeID == null || challengeID == '') {
    alert('No challenge ID specified.');
    window.location.href = '/pages/home.html';
}

function correctnessChanged(qid) {
    [... document.getElementsByClassName('correctnessq'+qid)].forEach((e)=>{
        console.log(document.getElementById('correctnessq'+qid).value)
        e.innerHTML = document.getElementById('correctnessq'+qid).value + "%"
    })
}

function saveEvaluation(qid) {
    fetch(API_URL + '/challenges/'+challengeID+'/save/enrollments/'+userID+'/solutions/'+qid, {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify({
            correctness: document.getElementById('correctnessq'+qid).value
        })
    })
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        window.alert('Evaluation saved successfully!');
    })
}

function showQuestions() {
    fetch(API_URL + '/challenges/'+challengeID+'/view/enrollments/'+userID+'/solutions', {
        method: 'GET',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    })
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        var questions = resp.questions;
        Object.keys(questions).forEach((key)=>{
            document.getElementById('questions').innerHTML += `
            <div style="margin: 10px;">
                <div style="border: 1px solid #ff00bb; padding: 10px;">
                    Question <span style="color: #ff00bb; font-weight: bold;">`+key+`</span>
                    <br>
                    User Solution<br>
                    <div style="display: flex;">
                        <div style="max-height: 60vh; width: 45%; overflow: scroll;">
                            <code style="background-color: #000;">
                                `+ escapeHtml(questions[key].code)+`
                            </code>
                        </div>
                        <div style="width: 55%; height: 60vh; display: flex; flex-direction: column; justify-content: space-between;">
                            <div style="height: 15%; overflow-y: scroll; word-wrap: break-word; border: 1px solid #ff00bb; padding: 10px;" id="question-current-ques">`+questions[key].question+`</div>
                            <div style="height: 45%;">
                                <iframe id="currentcodedisp`+key+`" style="width: 99.5%; height: 99.4%; background-color: aliceblue;"></iframe>
                            </div>
                            <div style="border: 1px solid #ff00bb; height: 40%; padding: 5px;">
                                <b>Expected Output:</b>
                                <div style="display: flex; align-items: center; height: 90%;">
                                    <img id="questionmediadispimg`+key+`" style="height: 99%;">
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div style="display: flex; justify-content: space-evenly;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div>
                                Correctness: <span style="color: #ff00bb; font-weight: bold;" class="correctnessq`+key+`">`+questions[key].correctness+`%</span>
                            </div>
                            <input type="range" min="0" max="100" value="`+questions[key].correctness+`" class="slider" id="correctnessq`+key+`" oninput="correctnessChanged(`+key+`)" autocomplete="off">
                            <button style="background-color: #ff00bb; font-size: .9rem; color: rgb(14, 7, 37);" onclick="saveEvaluation(`+key+`)">
                                Save
                            <br>
                        </div>
                        <div>
                            Last Evaluated by <span style="color: #ff00bb; font-weight: bold;" class="lastevaluatedbyq1">`+questions[key].evaluationBy+`</span>
                            on <span style="color: #ff00bb; font-weight: bold;" class="lastevaluatedonq1">`+questions[key].evaluationOn+`</span>
                        </div>
                    </div>
                </div>
            </div>
            `;
            document.getElementById('currentcodedisp'+key).srcdoc = questions[key].code;
            document.getElementById('questionmediadispimg'+key).src = questions[key].questionFileLink;
            correctnessChanged(key);
        })
    })
}

showQuestions()