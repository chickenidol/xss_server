let prevAdmHeader = false;

function getP(content, className = ""){
	let paragraph = document.createElement('p')
	paragraph.textContent = content

	if (className.length){
		paragraph.classList.add(className)
	}

	return paragraph
}

function downloadFile(uid, fileName){
	fetch(HOSTURL + '/chat/download/' + uid)
	.then((response) => response.blob())
	.then((blob) => {
		const url = window.URL.createObjectURL(new Blob([blob]))
		const a = document.createElement('a')
		a.href = url
		a.download = fileName
		document.body.appendChild(a)
		a.click()
		window.URL.revokeObjectURL(url)
	})
	.catch((error) => console.error('Error:', error))
}

function clearChat(){
	let messages = document.getElementById('messages')
	messages.innerHTML = ""
}

function appendMessage(messageText, preheader = "") {
	let messages = document.getElementById('messages')
	let message = document.createElement('div')
	message.className = 'MyMessage'

	const data = JSON.parse(messageText);

	if (data['operation'] == 'file'){
		data['fileName'] = decodeURIComponent(data['fileName'])
		if (CLIENT_ID === data['sourceClientId']) {
			message.appendChild(getP("You have uploaded file: " + data['fileName']))
			message.className = 'MyMessage'
			messages.appendChild(message)
			prevAdmHeader = false
		}
		else {
			if (!prevAdmHeader && preheader.length) {
				messages.appendChild(getP(preheader, "admin_header"))
			}

			message.className = 'OtherMessage'
			mainFileBlock = document.createElement('div')
			fileNameBlock = document.createElement('span')
			fileNameBlock.textContent = data['fileName']

			let downloadBtn = document.createElement('button')
			downloadBtn.textContent = 'Download'
			downloadBtn.classList.add('downloadButton')
			downloadBtn.addEventListener('click', function() {downloadFile(data['fileUid'], data['fileName'])})
			fileButtonBlock = document.createElement('span')
			fileButtonBlock.appendChild(downloadBtn)
			mainFileBlock.appendChild(fileNameBlock)
			mainFileBlock.appendChild(fileButtonBlock)
			message.appendChild(mainFileBlock)
		}
	}
	else if (data['operation'] == 'msg'){
		data['text'] = decodeURIComponent(data['text'])

		if (CLIENT_ID === data['sourceClientId']) {
			prevAdmHeader = false
			message.appendChild(getP(data['text']))
			message.className = 'MyMessage'
		} else {
			if (!prevAdmHeader && preheader.length) {
				messages.appendChild(getP(preheader, "admin_header"))
				prevAdmHeader = true
			}

			message.appendChild(getP(data['text']))
			message.className = 'OtherMessage'
		}
	}

	messages.appendChild(message)
	messages.scrollTop = messages.scrollHeight - messages.clientHeight
}


function sendMessage(event) {
	let input = document.getElementById('messageText')
	if (input.value.length) {
		let data = {
			"operation": "msg",
			"sourceClientId": CLIENT_ID,
			"destClientId": DEST_CLIENT_ID,
			"text": encodeURIComponent(input.value)
		}
		if (ws && ws.readyState == 1){
			ws.send(JSON.stringify(data))
		}

		input.value = ''
	}

	event.preventDefault()
}

function handleFileSelect(event) {
	let file = event.target.files[0]
	event.preventDefault()
	if (file) {
		let reader = new FileReader()
		reader.onload = function (e) {
			let data = {
				"operation": "file",
				"sourceClientId": CLIENT_ID,
				"destClientId": DEST_CLIENT_ID,
				"fileName": file.name,
				"content": e.target.result
			}
			ws.send(JSON.stringify(data))
		}
		reader.readAsDataURL(file)
	}
}

function attachCss(cssLocation, cssId, noCache = 0){
	if (!document.getElementById(cssId)) {
		let ts = ""
		if (noCache)
			cssLocation = cssLocation + "?ts=" + new Date().getTime()

		let head = document.getElementsByTagName('head')[0]

		let link = document.createElement('link')
		link.id = cssId
		link.rel = 'stylesheet'
		link.type = 'text/css'
		link.href = cssLocation
		link.media = 'all'

		head.appendChild(link)
		return link
	}
}