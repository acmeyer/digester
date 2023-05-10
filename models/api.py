from pydantic import BaseModel

class NewMessageRequest(BaseModel):
    message: str