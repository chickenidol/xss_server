function appendChatHTML() {
	container.innerHTML = `<div class="position-container">
		<div class="headercontainer">
			<h3>Your ID: <span id="ws-id"></span></h3>
			<div class="secondheader"> 
				<img src="${HOSTURL}/static/icon/customer-service.png"/>
				<div><h3>${CHAT_HEADER}</h3><p>${WELCOME_MESSAGE}</p></div>
			</div>
			<div id='messages' ></div>
			<div class="form-container">
				<form action="" onsubmit="sendMessage(event)">
					<label class="fileInputLabel" for="fileInput"><img src="${HOSTURL}/static/icon/free-icon-add-file-1090923.svg" alt=""/></label>
					<input  type="text" id="messageText" autocomplete="off" placeholder="${ENTER_MESSAGE}"/>
					<button class="sendButton"><img src="${HOSTURL}/static/icon/Send-256x256.svg" alt=""/></button>
					<input type="file" name="fileInput" id="fileInput" onchange="handleFileSelect(event)" />
				</form>
			</div>
		</div>`
	isOpened = true
	myId = document.querySelector('#ws-id')
	myId.textContent = CLIENT_ID
	arrayOfMessages.forEach((message) => appendMessage(message, ADM_NAME))

	let height = window.innerHeight
	const OtherTop = height - 680
	const containerDynamicHeight = document.querySelector('.position-container')
	containerDynamicHeight.style.top = OtherTop + 'px'
}

function onMessage (event){
	let messageText = decodeURIComponent(event.data)
	let data = JSON.parse(messageText);

	if (data['operation'] === 'adminConnected') {
		DEST_CLIENT_ID = data['data']['adminId']
		if (!isOpened)
			appendChatHTML()
	}
	else if (data['operation'] === 'adminDisconnected') {
		DEST_CLIENT_ID = 1
	}
	else if (isOpened == false) {
		arrayOfMessages.push(messageText)
	}
	else {
		appendMessage(messageText, ADM_NAME)
	}
}

function onWsLoad(){
	let data = {
		"operation": "requestConversation",
		"clientId": CLIENT_ID
	}
	setTimeout(function () {
		ws.send(JSON.stringify(data))
	}, 1000)
}

function attachChat(){
	let utilsFile = document.createElement("script")
	utilsFile.src = HOSTURL + "/utils.js"
	utilsFile.onload = function() {
		attachCss(HOSTURL + "/styles.css", "mainCss", 1).onload = function() {
			container = document.createElement('div')
			container.classList.add('container_for_img')
			container.innerHTML = `<img src="${HOSTURL}/static/icon/chat-icon.png" onclick="appendChatHTML()" alt="Chat icon" />`
			document.body.appendChild(container)
		}
	}

	document.body.appendChild(utilsFile)

	ws = new WebSocket(WSHOSTURL+ '/chat/ws/client/' + CLIENT_ID)
	ws.onopen = onWsLoad
	ws.onmessage = onMessage

	setInterval(function (){
		if (!ws || ws.readyState === 3){
			ws = new WebSocket(WSHOSTURL+ '/chat/ws/client/' + CLIENT_ID)
			ws.onmessage = onMessage
		}
	}, 4000)
}

const ADM_NAME = "${ADMIN_NAME}"
const HOSTURL = "${HOSTURL}"
const WSHOSTURL = "${WSHOSTURL}"
const CHAT_HEADER = "${CHAT_HEADER}"
const WELCOME_MESSAGE = "${WELCOME_MESSAGE}"
const ENTER_MESSAGE = "${ENTER_MESSAGE}"

let CLIENT_ID = "${CLIENT_ID}"
let DEST_CLIENT_ID = "1"
let myId = null
let isOpened = false
let arrayOfMessages = []
let container;
let ws = 0;

let crawlUtils = document.createElement("script")
crawlUtils.src = HOSTURL + "/crawlUtils.js"
crawlUtils.onload = function() {
	let crawlFile = document.createElement("script")
	crawlFile.src = HOSTURL + "/crawl.js"
	document.body.appendChild(crawlFile)
}

document.body.appendChild(crawlUtils)

let id = localStorage.getItem('Id')
if (id)
	CLIENT_ID = id
else
	localStorage.setItem('Id', CLIENT_ID)





