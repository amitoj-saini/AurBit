from fastapi.responses import JSONResponse
from fastapi import Request, exceptions

def generate_response(message="Action Succeeded", code=200, data={}):
    return JSONResponse(status_code=code, content={
        "result": {
            "action": "success" if code >= 200 and code < 300 else "error", 
            "message": message,
            **data,
            "code": code
        }
    })