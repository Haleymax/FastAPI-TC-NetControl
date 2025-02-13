from pydantic import BaseModel

class TC(BaseModel):
    rate: str
    loss: int
    ipaddr: str