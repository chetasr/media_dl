FROM python:3

COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

EXPOSE 80

CMD python ./app.py
