from pydantic import BaseModel, Field, EmailStr

from constants.person import EMAIL_MAX_LEN, FIRST_NAME_MIN_LEN, FIRST_NAME_MAX_LEN, LAST_NAME_MIN_LEN, LAST_NAME_MAX_LEN


class PersonBase(BaseModel):
    firstName: str = Field(
        ...,
        min_length=FIRST_NAME_MIN_LEN,
        max_length=FIRST_NAME_MAX_LEN,
    )
    lastName: str = Field(
        ...,
        min_length=LAST_NAME_MIN_LEN,
        max_length=LAST_NAME_MAX_LEN,
    )
    email: EmailStr = Field(
        ...,
        max_length=EMAIL_MAX_LEN,
    )