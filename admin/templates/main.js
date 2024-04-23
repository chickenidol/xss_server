function updateState(users = []){
	let state = document.getElementById('state')
	let block = document.createElement("div")

	block.appendChild(getP("Admin ID: " + CLIENT_ID))

	if (DEST_CLIENT_ID){
		block.appendChild(getP("In conversation with: " + DEST_CLIENT_ID))
	}

	if (users.length){
		block.appendChild(getP("Users connected: " + users.length))

		for (let i = 0; i < users.length; i++)
			block.appendChild(getP("User: " + users[i]))
	}

	state.innerHTML = ""
	state.appendChild(block)
}

function onMessage (event){
	setTimeout(function(){
		appendMessage(decodeURIComponent(event.data), "client")
	}, 100)
}

function onControlMessage (event){
	data = JSON.parse(event.data)

	if (data['operation'] == "userConversationData"){
		appendMessage(JSON.stringify(data['data']), "client")
	}
	else if (data['operation'] == "usersUpdate"){
		CreateOptions(data['data'])
		updateState(data['data'])
	}
}

function sendControlData(data){
	if (controlWs && controlWs.readyState == 1)
		controlWs.send(JSON.stringify(data))
}
function requestConversationData(){
	sendControlData({
		"operation": "getConversationData",
		"clientId": DEST_CLIENT_ID
	})
}

function updateUsers(){
	sendControlData({
		"operation": "getClients"
	})
}

function setConversation(clientId){
	DEST_CLIENT_ID = clientId
	let data = {
		"operation": "setConversation",
		"clientId": clientId
	}

	sendControlData(data)

	ws = new WebSocket(WSHOSTURL + '/chat/ws/client/' + CLIENT_ID + '/'  + TOKEN)
	ws.onmessage = onMessage
	ws.onopen = requestConversationData
}

function releaseConversation(){
	sendControlData({
		"operation": "releaseConversation",
		"clientId": DEST_CLIENT_ID
	})

	DEST_CLIENT_ID = ""
	ws.close()
}

function htmlEnc(s) {
  return s.replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/'/g, '&#39;')
    .replace(/"/g, '&#34;');
}

function CreateOptions(chats){
	if (PageState != 'chats')
		return

	document.getElementById('chats').innerHTML = ""

	for (let i = 0; i < chats.length; i++) {
		let chat = chats[i]

		const userDiv = document.createElement('div')
		const innerText = document.createElement('p')
		innerText.textContent = chat
		innerText.classList.add('Inner_chats_text')
		userDiv.classList.add('user-div')
		userDiv.appendChild(innerText)

		userDiv.addEventListener('click', (e) => {
			setConversation(chat)
			e.preventDefault()

			PageState = 'chat'
			container.innerHTML = `<div class="position-container"> 
				<div class="headercontainer" style="display:flex;align-items: center" >
					<img src="/static/icon/Vector.svg" class="BackArrow" />
					<h3 style="margin: 0px 105px;">ID Собеседника: 
						<span id="ws-id">${htmlEnc(DEST_CLIENT_ID)}</span>
					</h3>
				</div>
				<div id='messages' ></div>
				<div class="form-container">
					<form action="" onsubmit="sendMessage(event)">
						<label class="fileInputLabel" for="fileInput">
							<img src="/static/icon/free-icon-add-file-1090923.svg" alt=""/>
						</label>
						<input  type="text" id="messageText" autocomplete="off" placeholder="Enter your message"/>
						<button class="sendButton"><img src="/static/icon/Send-256x256.svg" alt=""/></button>
						<input type="file" name="fileInput" id="fileInput" onchange="handleFileSelect(event)" />
					</form>
				</div>
			</div>`
			let img = document.getElementsByClassName('BackArrow')[0]
			img.addEventListener('click', () => {
				PageState = 'chats'
				releaseConversation()
				updateUsers()
				container.innerHTML = `<div class="position-container">
					<div class="headercontainer">
						<h3>Chats <span id="ws-id"></span></h3>
					</div>
					<div id='chats' ></div>
				</div>`
			})
		})

		document.getElementById('chats').appendChild(userDiv)
	}
}

async function controlCycle() {
	while (controlWs.readyState == 1){
		await timer(CONTROL_MESSAGE_TIMEOUT);
		updateUsers()
	}
}

const CONTROL_MESSAGE_TIMEOUT = 1000
const CONTROL_MESSAGE_RECONNECT_TIMEOUT = 2000
const container = document.getElementById('container')

let PageState = 'chats'
let TOKEN = "${TOKEN}"
let HOSTURL = "${HOSTURL}"
let WSHOSTURL = "${WSHOSTURL}"
let DEST_CLIENT_ID = ""
let CLIENT_ID = "${CLIENT_ID}"

let utilsFile = document.createElement("script")
utilsFile.src = HOSTURL + "/utils.js"
document.body.appendChild(utilsFile)

let controlWs = new WebSocket(WSHOSTURL + '/chat/ws/admin/'+ CLIENT_ID + '/' + TOKEN)
controlWs.onmessage = onControlMessage
controlWs.onopen = controlCycle

const timer = ms => new Promise(res => setTimeout(res, ms))

setInterval(function (){
	if (!controlWs || controlWs.readyState == 3){
		controlWs = new WebSocket(WSHOSTURL + '/chat/ws/admin/'+ CLIENT_ID + '/' + TOKEN)
		controlWs.onmessage = onControlMessage
		controlWs.onopen = controlCycle
	}
}, CONTROL_MESSAGE_RECONNECT_TIMEOUT)

setInterval(function (){
	if (DEST_CLIENT_ID.length && controlWs && controlWs.readyState == 1) {
		if (!ws || ws.readyState == 3){
			clearChat()
			setConversation(DEST_CLIENT_ID)
		}
	}
}, CONTROL_MESSAGE_RECONNECT_TIMEOUT)

