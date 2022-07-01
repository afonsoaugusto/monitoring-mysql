FROM python:3.9.13-slim-buster

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY monitor.py /src/monitor.py

EXPOSE 8000

CMD [ "python", "/src/monitor.py" ]
