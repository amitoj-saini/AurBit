from fastapi.responses import JSONResponse
from lib import db, responses
from fastapi import Request

async def path_validator(request: Request, call_next):
    if len(db.fetch_users()) == 0 and request.url.path != "/management/createuser":
        return responses.generate_response(
            message="AurBit hasn't been setup yet, create a user.",
            code=400
        )

    response = await call_next(request)
    return response