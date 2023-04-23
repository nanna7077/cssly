var challengeID = null;

function applyToAllMatchingClasses(classname, value) {
    [... document.getElementsByClassName(classname)].forEach((item) => {
        item.innerHTML = value;
    });
}

function setRestrictionTypes(restrictionType, status) {
    if (status) {
        document.getElementById(restrictionType).style.backgroundColor = 'green';
        document.getElementById(restrictionType).style.color = 'black';
        document.getElementById(restrictionType+'check').innerHTML = '';
    } else {
        document.getElementById(restrictionType).style.backgroundColor = 'red';
        document.getElementById(restrictionType).style.color = 'black';
        document.getElementById(restrictionType+'check').innerHTML = 'Not ';
    }
}

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
        
        applyToAllMatchingClasses('display-challenge-name', c.name);
        applyToAllMatchingClasses('display-challenge-description', c.description);
        applyToAllMatchingClasses('display-challenge-creator', c.creator);
        applyToAllMatchingClasses('display-challenge-startTime', c.startTime);
        applyToAllMatchingClasses('display-challenge-endTime', c.endTime);
        applyToAllMatchingClasses('display-challenge-questions', c.numberOfQuestions);
        applyToAllMatchingClasses('display-challenge-questionPool', c.questionPoolSize);

        setRestrictionTypes('tabswitchrestriction', c.isTabSwitchingRestricted);
        setRestrictionTypes('copypasterestriction', c.isCopyPasteRestricted);
        setRestrictionTypes('manualevaluation', c.isManuallyEvaluated);
        setRestrictionTypes('publicleaderboard', c.isPublicLeaderboard);
        setRestrictionTypes('inviteonly', c.inviteOnly);
        

        if (c.isClosed || c.ended) {
            document.getElementById('enroll-button').style.display = 'none';
            document.getElementById('start-button').style.display = 'none';
        }
        if (c.inviteOnly) {
            document.getElementById('enroll-button').innerHTML = 'Request to Enroll';
            document.getElementById('enroll-button').disabled = true;
        }
        if (c.enrolled) {
            document.getElementById('enroll-button').innerHTML = 'Already Enrolled';
            document.getElementById('enroll-button').disabled = true;
            if (! c.notStarted) {
                document.getElementById('start-button').style.display = 'block';
            }
        } else  {
            document.getElementById('enroll-button').style.display = 'block';
        }

        fetch(API_URL+'/challenges/view/'+challengeID+'/leaderboard', {
            method: 'GET',
            headers: new Headers({
                'WWW-Authenticate': localStorage.getItem('sessionkey'),
                'Bypass-Tunnel-Reminder': 'true'
            })
        })
        .then(resp => resp.json())
        .then((resp) => {
            var leaderboardTable = document.getElementById('leaderboard');
            if (resp.error != undefined) {
                leaderboardTable.innerHTML = resp.error;
                return;
            }
            var out = `
            <table>
                <tr>
                    <th style="padding: 10px;">Rank</th>
                    <th style="padding: 10px;">Username</th>
                    <th style="padding: 10px;">Score</th>
                </tr>
            `;
            Object.keys(resp.leaderboard).forEach((key) => {
                out += `
                <tr>
                    <td style="padding: 10px; color: #ff00bb; font-weight: bold;">`+key+`</td>
                    <td style="padding: 10px;">`+resp.leaderboard[key].username+`</td>
                    <td style="padding: 10px;">`+resp.leaderboard[key].score+`</td>
                </tr>`;
            });
            out += '</table>';
            leaderboardTable.innerHTML = out;
        });                

        if (c.isAdmin) {
            // document.getElementById('enroll-button').style.display = 'none';
            // document.getElementById('start-button').style.display = 'none';
            document.getElementById('adminextras').style.display = 'block';
            document.getElementById('currentadmins').innerHTML = c.currentAdmins.join(', ');

            // Show Enrolled Users
            fetch(API_URL+'/challenges/view/'+challengeID+'/enrollments/viewall', {
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
                var enrollmentTable = document.getElementById('currentenrolled');
                var out = ''
                Object.keys(resp.enrollments).forEach((key) => {
                    out += `
                    <tr>
                        <td>`+resp.enrollments[key].username+`</td>
                        <td>`+resp.enrollments[key].createdOn+`</td>
                        <td>`+resp.enrollments[key].startedOn+`</td>
                        <td>`+resp.enrollments[key].tabSwitchCount+`</td>
                        <td>`+resp.enrollments[key].copyPasteCount+`</td>`
                    if (resp.enrollments[key].isNotEvaluated) {
                        out += `
                            <td><a onclick="window.open('/pages/evaluate.html?cid=`+challengeID+`&uid=`+resp.enrollments[key].userID+`', '_target');"  onmouseover="this.style.color='#ff00bb';" onmouseleave="this.style.color='#fff';">Evaluate</a></td>
                            </tr>`;
                            //<a onclick="removeEnrollment('Test');" onmouseover="this.style.color='#ff00bb';" onmouseleave="this.style.color='#fff';">Remove Enrollment</a>
                    }
                    else {
                        out += `
                            <td><a onclick="window.open('/pages/evaluate.html?cid=`+challengeID+`&uid=`+resp.enrollments[key].userID+`', '_target');" style='color: green; font-weight: bold; background-color: white; padding: 2px;'>Evaluated</a></td>
                            </tr>`;
                    }
                    
                })
                enrollmentTable.innerHTML = `
                <table>
                    <tr>
                        <td>Username</td>
                        <td>Enrolled On</td>
                        <td>Started On</td>
                        <td>Tab Switch Count</td>
                        <td>Copy Paste Count</td>
                        <td>Action(s)</td>
                    </tr> `
                    + out +
                `</table>`;
            })

        }

    })
}

function enroll() {
    fetch(API_URL+'/challenges/'+challengeID+'/enroll',
        {
            method: 'POST',
            headers: new Headers({
                'WWW-Authenticate': localStorage.getItem('sessionkey'),
                'Bypass-Tunnel-Reminder': 'true'
            })
        }
    )
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        window.alert('Enrolled successfully!');
        window.location.reload();
    })
}

function startChallenge() {
    fetch(API_URL+'/challenges/'+challengeID+'/start', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    }
    )
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
        }
        window.location.href = '/pages/questionView.html?cid='+challengeID;
    })
}

function addAdmin() {
    var adminToAdd = document.getElementById('adminadd').value;

    fetch(API_URL+'/challenges/'+challengeID+'/addadmin', {
        method: 'POST',
        headers: new Headers({
            'WWW-Authenticate': localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify({
            adminToAdd: adminToAdd
        })
    })
    .then(resp => resp.json())
    .then((resp) => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        window.alert('Admin added successfully!');
        window.location.reload();
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

fetchChallenge();