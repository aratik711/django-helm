FROM aratik711/python:3.6

COPY git_ranger/ /opt/git_ranger
WORKDIR /opt/git_ranger
COPY entrypoint.sh .
COPY post_install.sh .
RUN chmod +x /opt/git_ranger/entrypoint.sh && \
    chmod +x /opt/git_ranger/post_install.sh

RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk del --no-cache .build-deps && \
    python3 manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["sh", "/opt/git_ranger/entrypoint.sh"]


