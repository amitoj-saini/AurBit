# create nesscary folders
from routers import users
from lib import initial
initial.setup()

from lib import configs, db, middleware
from fastapi import FastAPI
import uvicorn

# varibles
CONFIG = configs.fetch_server_config()
app = FastAPI()

app.middleware("http")(middleware.path_validator)
app.middleware("http")(middleware.auth_validator(CONFIG["PWD"]))

# routers
app.include_router(users.router, prefix="/users")

if __name__ == "__main__":
    db.init_db()
    uvicorn.run(app, host="127.0.0.1", port=CONFIG["PORT"])