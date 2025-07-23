from lib.db import create_new_user, create_user_session
from lib.responses import generate_response
from lib.middleware import login_required
from fastapi import APIRouter, Request
from pydantic import BaseModel

class CreateUser(BaseModel):
    displayName: str
    email: str
    access: int | None = None # inital user creation doesn't require
    password: str | None = None # initial user creation require


router = APIRouter()

@router.post("/")
@login_required(exception=lambda req: req.state.users_length == 0)
async def create_user(request: Request, user: CreateUser):
    # if no previous users ( allow super user creation )
    if not request.state.session and request.state.users_length == 0 and user.password:
        created_user = create_new_user(displayName=user.displayName, email=user.email, password=user.password, initialized=True, access=0)
        if create_user:
            created_session = create_user_session(created_user.id)
            return generate_response(data={
                "access_token": created_session.token
            }, code=200)
    else:
        pass
    
    return generate_response(message="User Creation Failed", code=500)