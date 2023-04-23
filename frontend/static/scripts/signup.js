function signup() {
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmpassword = document.getElementById("confirmpassword").value;

    fetch(API_URL + '/users/register', {
        method: 'POST',
        headers: new Headers({
            'Bypass-Tunnel-Reminder': 'true'
        }),
        body: JSON.stringify({
            "username": username,
            "email": email,
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
        window.alert(resp.message);
        window.location.href = '/pages/login.html';
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