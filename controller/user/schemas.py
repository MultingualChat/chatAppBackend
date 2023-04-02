from pydantic import BaseModel, EmailStr
from typing import Optional


class UserEdit(BaseModel):
    nickname: Optional[str]
    avatar: Optional[str]
    language: Optional[str]


class UserObjResponse(BaseModel):
    email: EmailStr
    nickname: str
    avatar: str
    language: str


class UserCreateResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserObjResponse


class User(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    language: str
    avatar: str

    def to_json(self):
        return {
            "nickname": self.nickname,
            "email": self.email,
            "language": self.language,
            "avatar": self.avatar
        }
