from pydantic import BaseModel

class TC(BaseModel):
    rate: str
    delay: int
    loss: int