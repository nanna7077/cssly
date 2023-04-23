function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    fetch(API_URL + '/users/login', {
        method: 'POST',
        headers: new Headers({
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify({
            "username": username,
            "password": password,
        },
        )
    })
    .then((resp)=>resp.json())
    .then((resp)=>{
        if (resp.error != undefined) {
            window.alert(resp.error);
            return;
        }
        window.localStorage.setItem("sessionkey", resp.sessionkey);
        window.alert(resp.message);
        window.location.href = '/pages/home.html';
    })
}

// Add credits

var credits = document.createElement('div');
credits.style.bottom = '0';
credits.style.width = '95%';
credits.style.textAlign = 'center';
credits.style.position = 'absolute';
credits.style.color = 'white';
credits.style.backgroundColor = 'rgba(255, 255, 255, .5);';
credits.style.padding = '10px';
credits.innerHTML = 'Made with &heartsuit; by <a href="https://github.com/nanna7077/" style="color: #ff00bb;">Nannan</a>';

document.body.appendChild(credits);