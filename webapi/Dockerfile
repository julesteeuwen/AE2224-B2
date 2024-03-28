# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY AE2224-B2/webapi/requirements.txt AE2224-B2/webapi/requirements.txt
RUN pip3 install -r AE2224-B2/webapi/requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app=AE2224-B2/webapi/app.py", "run", "--host=0.0.0.0"]