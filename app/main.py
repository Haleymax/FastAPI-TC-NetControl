from fastapi import FastAPI
import uvicorn

from app.views import views

app = FastAPI()
app.include_router(views.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)