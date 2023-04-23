fetch(API_URL + '/challenges/view/global/leaderboard', {
    method: 'GET',
    headers: {
        'WWW-Authenticate': window.localStorage.getItem('sessionkey'),
        'Bypass-Tunnel-Reminder': 'true'
    }
})
.then(response => response.json())
.then(resp => {
    var leaderboardTable = document.getElementById('globalLeaderboard');
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
                <td style="padding: 10px; color: #ff00bb; font-weight: bold;">`+ key + `</td>
                <td style="padding: 10px;">`+ resp.leaderboard[key].username + `</td>
                <td style="padding: 10px;">`+ resp.leaderboard[key].score + `</td>
            </tr>`;
    });
    out += '</table>';
    leaderboardTable.innerHTML = out;
})

var secondCount = 1;
setInterval(()=>{
    if (secondCount == 10) window.location.reload();
    else document.getElementById('refreshTimer').innerHTML = 10 - secondCount;
    secondCount++;
}, 1000);