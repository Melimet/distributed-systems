import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

class ClientServer:
    def __init__(self, host):
        self.host = host
        self.client = httpx.AsyncClient()
        print("ClientServer initialized")

    async def handle(self, request: Request):

        ##TODO Implement sending the request to the correct node          
        response = request.method + " " + request.url.path 

        return response
