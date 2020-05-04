FROM python:3.8

RUN python -m pip install --upgrade pip

COPY yt-classifier /yt-classifier

COPY init.sh /init.sh

RUN /bin/bash /init.sh && \
	python -m pip install -r /yt-classifier/requirements.txt


WORKDIR /yt-classifier
EXPOSE 5000

VOLUME /var/lib/yt-classifier
ENV AUTODETECT_CPU=1 
CMD [ "python", "/yt-classifier/run.py" ]
