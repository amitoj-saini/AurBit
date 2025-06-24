from fastapi import Request, Response, status
from lib import db, responses, functions

def pwd_validator(pwd):
    async def middleware(request: Request, call_next):
        incoming_pwd = request.headers.get("pwd")
        if incoming_pwd == pwd:
            return await call_next(request)
        else:
            limit = functions.leaky_rate_limiter(unauthorized_attempts=5, within=300, penalty=20, url="*", ip_addr=request.client.host)
            if limit: return limit
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return middleware

async def path_validator(request: Request, call_next):
    if len(db.fetch_users()) == 0 and request.url.path != "/management/createuser":
        return responses.generate_response(
            message="AurBit hasn't been setup yet, create a user.",
            code=400
        )

    return await call_next(request)