FROM python:bullseye

WORKDIR /work 
COPY requirements.txt .

RUN pip install -r requirements.txt && pip install https://github.com/egbertbouman/youtube-comment-downloader/archive/master.zip 

ADD .. /work


CMD [ "flask","run","--host","0.0.0.0","--port","5000" ]



