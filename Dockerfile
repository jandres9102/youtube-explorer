FROM python

WORKDIR /work 

ADD . /work

RUN pip install -r requirements.txt && pip install https://github.com/egbertbouman/youtube-comment-downloader/archive/master.zip 

CMD [ "python3","scripts/__main__.py" ]

