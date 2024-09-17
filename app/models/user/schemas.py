from datetime import datetime
from typing import Annotated, ClassVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, model_validator

from app.functions.exceptions import unprocessable_entity
from app.models.auth.role import Role


class UserIn(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        json_schema_extra={
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "example@example.com",
                "username": "johndoe",
                "password": "password",
                "phone_number": "08012345678",
                "gender": "male",
                "date_of_birth": "2000-01-01",
                "avatar": "https://example.com/avatar.png",
                "level": "100",
                "cgpa": "4.0",
                "matric_number": "123456789",
                "institution": "University of Example",
                "faculty": "Science",
                "department": "Computer Science",
            },
        }
    )
    firstName: str
    lastName: str
    email: EmailStr
    username: str
    password: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    phone_number: str
    gender: str
    date_of_birth: str
    avatar: str
    level: str
    cgpa: str
    matric_number: str
    institution: str
    faculty: str
    department: str
    verified: bool = False
    scope: list[Role] = [Role.USER]


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    created_at: datetime
    updated_at: datetime
    firstName: str
    lastName: str
    email: EmailStr
    username: str
    phone_number: str
    gender: str
    date_of_birth: str
    avatar: str
    level: str
    cgpa: str
    matric_number: str
    institution: str
    faculty: str
    department: str
    verified: bool
    scope: list[Role]


class PasswordsIn(BaseModel):
    password: SecretStr = Field(..., examples=["123"])
    confirm_password: SecretStr = Field(..., examples=["123"])

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password.get_secret_value() != self.confirm_password.get_secret_value():
            raise unprocessable_entity("Passwords do not match")
        return self
