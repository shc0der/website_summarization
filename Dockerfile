FROM python:3.11.9-slim

RUN pip install --no-cache-dir --upgrade pip

EXPOSE 7860
ENV APP_HOME=/home

WORKDIR $APP_HOME

COPY ./app ./app
COPY ./data ./data
COPY ./.env ./
COPY ./requirements.txt ./
COPY ./docker-entrypoint.sh ./

RUN chmod +x ./docker-entrypoint.sh

RUN pip install -r requirements.txt &&\
    rm -rf /root/.cache/pip &&\
    rm requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]