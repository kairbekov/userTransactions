FastAPI simple project of User Transactions

How to start:
1. git clone [url]
2. python -m venv venv
3. source venv/bin/activate
4. python -m pip install pip==22.0.4 setuptools==62.1.0 wheel==0.37.1
5. python -m pip install -e .[dev,test]
6. python -m user_app

How to start docker container
1. git clone [url]
2. cd userTransactions
3. docker build -t user_app .
4. docker run -d --publish 8000:8000 --name test_app_container user_app