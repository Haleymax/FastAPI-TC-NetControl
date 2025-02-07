from fastapi import APIRouter



router = APIRouter()

@router.get("/hello")
def index():
    return {"message": "Hello World"}


