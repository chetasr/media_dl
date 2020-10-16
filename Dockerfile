FROM python:3.8

COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443
EXPOSE 88
EXPOSE 8443

CMD python ./app.py
