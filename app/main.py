from fastapi import FastAPI
import uvicorn

from app.api.endpoints import home, throttling
from app.core.settings import start_host

app = FastAPI()
app.include_router(home.router)
app.include_router(throttling.tc_router)



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


def execute():
    uvicorn.run(app, host=start_host, port=8009)
