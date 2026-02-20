from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


# -------- User --------

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# -------- Token --------

class Token(BaseModel):
    access_token: str
    token_type: str

# --------Listing----------
class ListingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: int

class OwnerResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ListingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int
    owner: OwnerResponse

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    listing_id: int
    start_date: date
    end_date: date

class BookingResponse(BaseModel):
    id: int
    listing_id: int
    user_id: int
    start_date: date
    end_date: date

    class Config:
        from_attributes = True

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
