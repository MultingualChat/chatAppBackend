from pydantic import BaseModel


class Config(BaseModel):
    JWT_SECRET = "easychat"


config = Config()
