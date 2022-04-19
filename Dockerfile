FROM python:bullseye

WORKDIR /work 
COPY requirements.txt .

RUN pip install -r requirements.txt && pip install https://github.com/egbertbouman/youtube-comment-downloader/archive/master.zip 

ADD . /work


CMD [ "python3","-u","analyse/description.py" ]
# CMD [ "python3","scripts/__main__.py" ]

