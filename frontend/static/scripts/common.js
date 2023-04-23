//API_URL = "http://csslybackend.loca.lt"
API_URL = "http://localhost:5000"

const escapeHtml = (unsafe) => {
    return unsafe.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;').replaceAll("\n", "<br>").replaceAll(" ", "&nbsp;");
}

function logout() {
    fetch(API_URL + "/users/logout", {
        method: "POST",
        headers: {
            "WWW-Authenticate": window.localStorage.getItem('sessionkey'),
            'Bypass-Tunnel-Reminder': 'true'
        }
    })
    .then(resp => resp.json())
    .then(resp => {
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
    })
    window.localStorage.removeItem('sessionkey');
    window.location.reload();
}

function colorAdder(initText) {
    var ret = '';
    [... initText.matchAll(/[A-Fa-f0-9]{6}/g)].forEach((match) => {
        ret += `<span style="background-color: #${match[0]}; margin-right: 5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>`;
    });
    return ret;
}