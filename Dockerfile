FROM python
RUN apt update && apk upgrade
RUN pip3 install "fastapi[all]"
RUN git clone https://github.com/chickenidol/xss_server.git
RUN cd /xss_server && pip install -r requirements.txt
RUN cd /xss_server/client && uvicorn app.main:app
EXPOSE 8000
