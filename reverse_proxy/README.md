# Reverse proxy


## How to run 
Install by running
```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

Start it via `uvicorn main:app --reload`


## How to use

When the complete application is up via docker compose, you can send requests to reverse proxy with a tool such as postman. There is a postman.json in the root files which can be imported and used to test out the api.

