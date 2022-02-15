FROM python

WORKDIR /work 

ADD . /work

RUN pip install -r requirements.txt

CMD [ "python3","scripts/lecteur.py" ]

