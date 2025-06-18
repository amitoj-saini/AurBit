from fastapi.responses import JSONResponse

def generate_response(message="Action Succeeded", code=200):
    return JSONResponse(status_code=code, content={
        "result": {
            "action": "success" if code >= 200 and code < 300 else "error", 
            "message": message,
            "code": code
        }
    })