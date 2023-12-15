from fastapi import FastAPI, Request    
from client_server import ClientServer   
    
app = FastAPI()    
    
client_server = ClientServer('http://localhost:8000')    
    
@app.get("/{path:path}")  
@app.post("/{path:path}")  
@app.put("/{path:path}")  
@app.delete("/{path:path}")  
async def root(path: str, request: Request):    
    return await client_server.handleRequest(request)    