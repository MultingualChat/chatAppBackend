from pydantic import BaseModel


class FieldError(BaseModel):
    msg: str = "Something went wrong"
    title: str = "Invalid input"
    key_name: str = "field"

    def json(self):
        return {
            self.key_name: self.msg,
        }