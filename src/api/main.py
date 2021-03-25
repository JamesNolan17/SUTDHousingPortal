from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from markkk.logger import logger

from .routes import application_periods, applications, auth, events, records, students

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(application_periods.router)
app.include_router(applications.router)

app.include_router(events.router)
app.include_router(records.router)


@app.get("/api")
async def index():
    return {"Hello": "SUTD Housing Portal"}
