FROM aratik711/python:3.6

COPY git_ranger/ /opt/git_ranger
WORKDIR /opt/git_ranger

RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk del --no-cache .build-deps && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate

EXPOSE 8000
ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000


