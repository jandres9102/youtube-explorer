FROM python:bullseye

WORKDIR /work 

RUN apt-get update && apt-get -y install cmake protobuf-compiler && apt-get -y install libgl1 && pip install dlib

COPY requirements.txt .

RUN apt install -y ffmpeg && pip install -r requirements.txt && pip install https://github.com/egbertbouman/youtube-comment-downloader/archive/master.zip 

ADD . /work


# CMD [ "python3","-u","analyse/description.py" ]
# CMD [ "python3","scripts/__main__.py" ]
CMD [ "bash","main.sh" ]

