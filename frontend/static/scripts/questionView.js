var challengeID = null;
var challengeGlobal = null;
var questionID = 1;

function applyToAllMatchingClasses(classname, value) {
    [... document.getElementsByClassName(classname)].forEach((item) => {
        item.innerHTML = value;
    });
}

function reloadCodePreview() {
    var content = document.editor.getValue();

    document.getElementById('currentcodedisp').srcdoc = content;
}

function saveCurrentCode() {
    document.getElementById('savecodebutton').innerHTML = 'Saving...';
    fetch(API_URL + '/challenges/'+challengeID+'/view/questions/'+questionID+'/save', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify({
            code: document.editor.getValue()
        })
    })
    .then(resp => resp.json())
    .then((resp)=> {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        var switchSaveModeStatus = false;
        var switchSaveMode = setInterval(() => {
            document.getElementById('savecodebutton').innerHTML = 'Saved';
            if (switchSaveModeStatus) {
                document.getElementById('savecodebutton').innerHTML = 'Save';
                clearInterval(switchSaveMode);
            }
            switchSaveModeStatus = true;
        }, 2000)
    })
}

function changeQuestion(qid) {
    questionID = qid;
    fetchChallenge();
}

function copyPasteOccurred() {
    if (challengeGlobal.isCopyPasteRestricted) {
        window.alert('Copy Paste is restricted in this challenge.');
    }
    fetch(API_URL + '/challenges/'+challengeID+'/save/copypaste', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
    })
    .then(resp => resp.json())
    .then((resp)=> {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
    })
}

function focusLoss() {
    if (challengeGlobal.isTabSwitchingRestricted) {
        window.alert('TabSwitching is restricted in this challenge.');
    }
    fetch(API_URL + '/challenges/'+challengeID+'/save/tabswitch', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
    })
    .then(resp => resp.json())
    .then((resp)=> {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
    })
}

document.addEventListener('visibilitychange', (e)=>{
    if (document.visibilityState != "visible") focusLoss();
})

function fetchChallenge() {
    fetch(API_URL + '/challenges/view/'+challengeID,
        {
            method: 'GET',
            headers: new Headers({
                'WWW-Authenticate': localStorage.getItem('sessionkey'),
                'Bypass-Tunnel-Reminder': 'true'
            }),
        }
    )
    .then(resp => resp.json())
    .then((resp)=> {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        var c = resp.challenge;
        challengeGlobal = c;
        
        applyToAllMatchingClasses('display-challenge-name', c.name);
        applyToAllMatchingClasses('display-challenge-description', c.description);
        applyToAllMatchingClasses('display-challenge-creator', c.creator);
        applyToAllMatchingClasses('display-challenge-startTime', c.startTime);
        applyToAllMatchingClasses('display-challenge-endTime', c.endTime);

        // End Time Countdown Handler
        endTime = new Date(c.endTime).getTime();
        var x = setInterval(function() {

            // Get today's date and time
            var now = new Date().getTime();
          
            // Find the distance between now and the count down date
            var distance = endTime - now;
          
            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("challenge-time-counter").innerHTML = days + "d " + hours + "h "
            + minutes + "m " + seconds + "s ";
          
            // If the count down is finished, write some text
            if (distance < 0) {
              clearInterval(x);
              document.getElementById("challenge-time-counter").innerHTML = "EXPIRED";
              saveCurrentCode();
            }
          }, 1000);

    })

    fetch(API_URL + '/challenges/'+challengeID+'/view/questions', {
        method: 'GET',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    })
    .then(resp => resp.json())
    .then((resp)=> {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        
        document.getElementById('questionsbox').innerHTML = '';
        var n = 1;
        Object.keys(resp.questions).forEach((key) => {
            if (key == questionID || n == 1) {
                questionID = key;
                document.getElementById('questionsbox').innerHTML += `
                <div class="questionsbox questionsbox-active" onclick="changeQuestion(`+key+`)">`+n+`</div>`;
                document.getElementById('display-challenge-qnum').innerHTML = key;
                document.getElementById('question-current-ques').innerHTML = '<b>Question:</b> ' + resp.questions[key].question + "<br>" + colorAdder(resp.questions[key].question);
                if (resp.questions[key].questionMediaType == 0) {
                    document.getElementById('questionmediadisp').innerHTML += '<img src="'+resp.questions[key].questionFileLink+'" style="width: 100%; height: 100%; object-fit: contain;" ondragstart="return false;">';
                } else {
                    document.getElementById('questionmediadisp').innerHTML += `<video controls><source src=`+resp.questions[key].questionFileLink+` type="video/mp4"></video>`;
                }
                var codeinitsetupinterval = setInterval(() => {
                    if (document.editor == undefined) return;
                    else {
                        document.editor.setValue(resp.questions[key].code); 
                        reloadCodePreview();
                        clearInterval(codeinitsetupinterval);
                    }
                }, 1000)
            } else {
                document.getElementById('questionsbox').innerHTML += `
                <div class="questionsbox" onclick="changeQuestion(`+key+`)">`+n+`</div>`;
            }
            n += 1;
        })
    })
}

window.location.search.substr(1).split('&').forEach(function (item) {
    var s = item.split('=');
    if (s[0] === 'cid') {
        challengeID = s[1];
    }
})

if (challengeID == null || challengeID == '') {
    alert('No challenge ID specified.');
    window.location.href = '/pages/home.html';
}

// Disable Right Click

document.addEventListener('contextmenu', event => event.preventDefault());

fetchChallenge();
