if (window.localStorage.getItem("sessionkey") != null) {
    fetch(API_URL + '/is-logged-in', {
        method: 'GET',
        headers: new Headers({'WWW-Authenticate': window.localStorage.getItem("sessionkey"), 'Bypass-Tunnel-Reminder': 'true'}),
    })
    .then((resp)=>resp.json())
    .then((resp)=>{
        if (resp.error != undefined) {
            window.alert(resp.error);
            window.localStorage.removeItem("sessionkey");
            window.location.href = '/pages/login.html';
            return;
        }
        [... document.getElementsByClassName('display-username')].forEach((e)=>{
            e.innerHTML = resp.user.name;
        });
        [... document.getElementsByClassName('display-id')].forEach((e)=>{
            e.innerHTML = resp.user.id;
        });
        [... document.getElementsByClassName('display-email')].forEach((e)=>{
            e.innerHTML = resp.user.email;
        });
    })
} else {
    window.location.href = '/pages/login.html';
}