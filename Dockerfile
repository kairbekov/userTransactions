FROM python:3.10-buster
USER root
ENV LANG=en_US.utf8
ENTRYPOINT ["/opt/userTransactions/user_app"]
WORKDIR /opt/userTransactions/
EXPOSE 8000

COPY alembic.ini setup.* README.md /opt/userTransactions/
COPY user_app /opt/userTransactions/user_app

RUN cd /opt/userTransactions \
    python3 -m alembic upgrade head \
    python3 -m user_app 2>&1 | tee /var/log/userTransactions.log
