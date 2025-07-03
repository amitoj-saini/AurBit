from lib.middleware import login_required
from fastapi import APIRouter, Request
from pydantic import BaseModel
from lib.db import Session

class CreateUser(BaseModel):
    displayName: str
    email: str
    access: str | None = None
    password: str | None = None


router = APIRouter()

@router.post("/")
@login_required(exception=True)
async def create_user(request: Request, user: CreateUser):
    print(request.state.session)
    return {"success": "You've come to the right place"}