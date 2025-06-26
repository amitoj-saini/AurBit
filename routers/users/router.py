from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_user():
    return {"success": "You've come to the right place"}