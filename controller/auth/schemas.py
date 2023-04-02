from pydantic import BaseModel, EmailStr, Field


class LoginResponse(BaseModel):
	access_token: str
	token_type: str


class LoginBase(BaseModel):
	email: EmailStr
	password: str = Field(min_length=8, max_length=50)

	class Config:
		schema_extra = {
			"example": {
				"email": "n.s@hotmail.com",
				"password": "e8yJjdHk"
			}
		}
