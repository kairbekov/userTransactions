FROM python:3.9
RUN  mkdir /userTransactions
WORKDIR /userTransactions
EXPOSE 8000:8000
COPY .gitignore alembic.ini example.db README.md setup.cfg setup.py ./
COPY ./user_app /userTransactions/user_app
# RUN python -m venv venv
RUN python -m pip install pip==22.0.4 setuptools==62.1.0 wheel==0.37.1
RUN python -m pip install -e .[dev,test]
CMD ["python", "-m", "user_app"]