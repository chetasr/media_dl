FROM python:3

COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

CMD python ./app.py
