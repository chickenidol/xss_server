FROM python
RUN apt update
RUN pip3 install "fastapi[all]"
RUN git clone https://github.com/chickenidol/xss_server.git
COPY .env /xss_server/client
COPY crawl.js /xss_server/client/templates
RUN cd /xss_server && pip install -r requirements.txt
WORKDIR /xss_server/client
EXPOSE 80
ENTRYPOINT ["uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "80"]