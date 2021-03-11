from fastapi import Depends, FastAPI, HTTPException
from markkk.logger import logger

from .routes import apexs, applications, auth, events, records, students

app = FastAPI()

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(apexs.router)
app.include_router(applications.router)

app.include_router(events.router)
app.include_router(records.router)


@app.get("/")
async def index():
    return {"message": "Hello from SUTD Housing Portal"}
