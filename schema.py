from pydantic import BaseModel


class Response(BaseModel):
    question: str


