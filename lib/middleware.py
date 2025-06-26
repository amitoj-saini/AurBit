from fastapi import Request, Response, status
from lib import db, responses, functions
from functools import wraps

# validate authentication from user
def auth_validator(pwd):
    async def middleware(request: Request, call_next):
        auth = request.headers.get("authorization").removeprefix("Bearer ").strip()
        if auth == pwd:
            return await call_next(request)
        else:
            limit = functions.leaky_rate_limiter(unauthorized_attempts=5, within=300, penalty=20, url="*", ip_addr=request.client.host)
            if limit: return limit
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return middleware

# middleware for validating paths based off of aurbit contexts
async def path_validator(request: Request, call_next):
    # if no users created ( setup )
    if len(db.fetch_users()) == 0 and (request.url.path.rstrip("/") != "/users" or request.method != "POST"):
        return responses.generate_response(
            message="AurBit hasn't been setup yet, create a user.",
            code=400
        )

    return await call_next(request)

# function based middleware
def login_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        pass

    return wrapper