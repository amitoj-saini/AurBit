# create nesscary folders
from lib import initial
initial.setup()

from lib import configs, db, middleware
from fastapi import FastAPI
import uvicorn

# varibles
CONFIG = configs.fetch_server_config()
app = FastAPI()

app.middleware("http")(middleware.path_validator)
app.middleware("http")(middleware.pwd_validator(CONFIG["PWD"]))

@app.get("/")
def index():
    return {"message": "Everything seems to be in order"}

if __name__ == "__main__":
    db.init_db()
    uvicorn.run(app, host="127.0.0.1", port=CONFIG["PORT"])