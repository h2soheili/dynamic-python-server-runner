# websocket-pubsub
fastapi + websocket + pub/sub redis



Create the requirements.txt file:
`pip freeze > requirements.txt`


Run server: `uvicorn app.main:app --port 9000` <br>
Run server in dev mode: `uvicorn app.main:app --port 9000 --reload`

redis_client = redis.Redis(host='localhost', port=6379, db=5)

move redis conf to envs