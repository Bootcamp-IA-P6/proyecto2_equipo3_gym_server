from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TockenResponse(BaseModel):
    access_tocken: str
    token_type: str= "bearer"