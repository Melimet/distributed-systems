from fastapi import FastAPI, Request    
from client_server import ClientServer   
from messaging_server import MessagingServer    
import asyncio
from config import port, ip
import uvicorn

async def start_messaging_server():
    messaging_server = MessagingServer(ip, port)
    await messaging_server.start()

 
async def start_client_server():    

    app = FastAPI()    
    client_server = ClientServer(f'{ip}:8080')

    @app.get("/{path:path}")  
    @app.post("/{path:path}")  
    @app.delete("/{path:path}")  
    async def root(path: str, request: Request):    
        return await client_server.handle_request(request) 

    uvicorn.run(app, host=ip, port=8080)

async def main():
    await asyncio.gather(start_messaging_server(), start_client_server())
   
if __name__ == "__main__":
    asyncio.run(main())