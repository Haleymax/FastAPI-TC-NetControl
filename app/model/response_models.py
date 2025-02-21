from typing import Union, Any

from pydantic.v1 import BaseModel


class TCResponse(BaseModel):
    result: bool
    interface: str
    message: Union[str, Any]