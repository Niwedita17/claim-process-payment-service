import os
import logging
from pprint import pformat
from .database import init_db, get_session
from fastapi import FastAPI
from .routers.index import claimRouter,graphqlRouter
import redis.asyncio as redis

app = FastAPI()

log = logging.getLogger("uvicorn")

# from fastapi_limiter import FastAPILimiter
     
@app.on_event("startup")
def startup_event():
    log.info("Starting up...")
    # redisx = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    # FastAPILimiter.init(redisx)
    init_db()

@app.on_event("shutdown")
def shutdown_event():
    log.info("Shutting down...")
    
app.include_router(claimRouter)
app.include_router(graphqlRouter, prefix="/graphql")