from fastapi import FastAPI
from dotenv import load_dotenv
from .db.db import Base, engine
from .routers.github_webhook import router as github_webhook_router
from .routers.github_issues import router as github_issue_router
from .routers.tickets_router import router as tickets_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github_webhook_router)
app.include_router(github_issue_router)
app.include_router(tickets_router)

#Uncomment the following lines if you want to create the database tables at startup# 
@app.on_event("startup")
def create_tables():
     Base.metadata.create_all(bind=engine)
