from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.database.models import Role

limit10years = datetime.today().date() - timedelta(days=365 * 10)


class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    thurname: Optional[str] = Field(None, max_length=30)
    email: EmailStr
    phone: PhoneNumber
    birthday: Optional[date] = Field(None)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("birthday")
    def validate_birthday(cls, value: date) -> date:
        """
        The validate_birthday function ensures that the user is between 10 and 100 years old.
            Args:
                value (date): The birthday of the user.

        :param cls: Pass the class to which the field belongs
        :param value: date: Pass the value of the birthday attribute to be validated
        :return: The date value if the user is between 10 and 100 years old
        :doc-author: Trelent
        """
        today = datetime.today().date()
        if (today - value).days > (365 * 100):
            raise ValueError("User cannot be older than 100 years")
        elif (today - value).days < (365 * 10):
            raise ValueError("User cannot be younger than 10 years")
        return value


class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # new pydantic requirement

    id: int = 1
    name: str
    thurname: Optional[str] = Field(None)
    email: EmailStr
    phone: PhoneNumber
    birthday: Optional[date] = Field(None)
    notes: Optional[str] = Field(None)
    created_at: datetime
    updated_at: datetime

    # class Config:
    # from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=15)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=10)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # new pydantic requirement

    id: int = 1
    username: str
    email: EmailStr
    avatar: str
    role: Role

    # class Config:
    # from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
