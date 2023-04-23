function displayChallenges() {
    fetch(API_URL + '/challenges/view/all', {
        method: 'GET',
        headers: new Headers({
            'WWW-Authenticate': window.localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    })
    .then(resp => resp.json())
    .then((resp)=>{
        if (Object.keys(resp.challenges).length == 0) {
            document.getElementById("challenges").innerHTML = `
            <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">No Challenges Found</span>
            `;
        }
        Object.keys(resp.challenges).forEach((c_)=>{
            var c = resp.challenges[c_];
            document.getElementById("challenges").innerHTML += `
            <div style="border-radius: 4px; border: #ff00bb solid 1px; padding: 10px; width: fit-content; cursor: pointer;" onmouseover="this.style.borderColor = 'white';" onmouseleave="this.style.borderColor = '#ff00bb';" onclick="window.location.href='/pages/challenge.html?cid=`+c_+`';">
                <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">`+c.name+`</span>
                <br>
                <span style="font-size: .9rem;">Created By: <span style="color: #ff00bb;">`+c.creator+`</span></span>
                <br>
                <span>`+c.description+`</span>
                <br>
                <span>Starts at <span style="color: #ff00bb;">`+c.startTime+`</span> and ends at <span style="color: #ff00bb;">`+c.endTime+`</span> </span>
                <br>
                Questions: <span style="color: #ff00bb;">`+c.numberOfQuestions+`</span>&nbsp;&nbsp;&nbsp;|&nbsp;
                Question Pool Size: <span style="color: #ff00bb;">`+c.questionPoolSize+`</span>
            </div>
            <br>
            `;
        })
    })

    fetch(API_URL + '/challenges/view/enrolled', {
        method: 'GET',
        headers: new Headers({
            'WWW-Authenticate': window.localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    })
    .then(resp => resp.json())
    .then((resp)=>{
        if (Object.keys(resp.challenges).length == 0) {
            document.getElementById("enrolledchallenges").innerHTML = `
            <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">Not Enrolled in any Challenge's Yet</span>
            `;
        }
        Object.keys(resp.challenges).forEach((c_)=>{
            var c = resp.challenges[c_];
            document.getElementById("enrolledchallenges").innerHTML += `
            <div style="border-radius: 4px; border: #ff00bb solid 1px; padding: 10px; width: fit-content; cursor: pointer;" onmouseover="this.style.borderColor = 'white';" onmouseleave="this.style.borderColor = '#ff00bb';" onclick="window.location.href='/pages/challenge.html?cid=`+c_+`';">
                <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">`+c.name+`</span>
                <br>
                <span style="font-size: .9rem;">Created By: <span style="color: #ff00bb;">`+c.creator+`</span></span>
                <br>
                <span>`+c.description+`</span>
                <br>
                <span>Starts at <span style="color: #ff00bb;">`+c.startTime+`</span> and ends at <span style="color: #ff00bb;">`+c.endTime+`</span> </span>
                <br>
                Questions: <span style="color: #ff00bb;">`+c.numberOfQuestions+`</span>&nbsp;&nbsp;&nbsp;|&nbsp;
                Question Pool Size: <span style="color: #ff00bb;">`+c.questionPoolSize+`</span>
            </div>
            <br>
            `;
        })
    })

    fetch(API_URL + '/challenges/view/administering', {
        method: 'GET',
        headers: new Headers({
            'WWW-Authenticate': window.localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        })
    })
    .then(resp => resp.json())
    .then((resp)=>{
        if (Object.keys(resp.challenges).length == 0) {
            document.getElementById("administeringchallenges").innerHTML = `
            <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">Not Enrolled in any Challenge's Yet</span>
            `;
        }
        Object.keys(resp.challenges).forEach((c_)=>{
            var c = resp.challenges[c_];
            document.getElementById("administeringchallenges").innerHTML += `
            <div style="border-radius: 4px; border: #ff00bb solid 1px; padding: 10px; width: fit-content; cursor: pointer;" onmouseover="this.style.borderColor = 'white';" onmouseleave="this.style.borderColor = '#ff00bb';" onclick="window.location.href='/pages/challenge.html?cid=`+c_+`';">
                <span style="font-size: 1.2rem; color: #ff00bb; font-weight: bold;">`+c.name+`</span>
                <br>
                <span style="font-size: .9rem;">Created By: <span style="color: #ff00bb;">`+c.creator+`</span></span>
                <br>
                <span>`+c.description+`</span>
                <br>
                <span>Starts at <span style="color: #ff00bb;">`+c.startTime+`</span> and ends at <span style="color: #ff00bb;">`+c.endTime+`</span> </span>
                <br>
                Questions: <span style="color: #ff00bb;">`+c.numberOfQuestions+`</span>&nbsp;&nbsp;&nbsp;|&nbsp;
                Question Pool Size: <span style="color: #ff00bb;">`+c.questionPoolSize+`</span>
            </div>
            <br>
            `;
        })
    })
}

displayChallenges()