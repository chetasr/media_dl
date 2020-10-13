FROM python:3

COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443
EXPOSE 88
EXPOSE 8443

CMD python ./app.py
