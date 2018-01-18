FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./entrypoint.sh /entrypoint.sh
COPY ./src /app

COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./prestart.sh /app/prestart.sh
COPY ./requirements.txt /app/requirements.txt
