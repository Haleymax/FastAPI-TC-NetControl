from pydantic import BaseModel

class Base(BaseModel):
    rate: str
    loss: int
    ipaddr: str

class TC(BaseModel):
    incoming: Base
    outgoing: Base