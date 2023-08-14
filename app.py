from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder
from starlette.routing import Mount, Route

from accounts.endpoints import router
from admin.config import ADMIN
from forum.routers import forum_router
from home.endpoints import HomeEndpoint

app = FastAPI(
    title="Simple headless forum",
    routes=[
        Route("/", HomeEndpoint),
        Mount("/admin/", ADMIN),
    ],
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(forum_router)


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
