from fastapi import FastAPI
from lib import configs
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Everything seems to be in order"}

if __name__ == "__main__":
    CONFIG = configs.fetch_server_config()
    uvicorn.run(app, host="127.0.0.1", port=CONFIG["PORT"])
    print(CONFIG)