from lib.middleware import login_required
from fastapi import APIRouter, Request
from lib.db import Session

router = APIRouter()

@router.post("/")
@login_required(exception=True)
async def create_user(request: Request):
    print(request.state.session)
    return {"success": "You've come to the right place"}