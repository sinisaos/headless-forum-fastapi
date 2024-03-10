from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder
from starlette.routing import Mount

from api.accounts.routers import router
from api.admin.config import ADMIN
from api.forum.routers import forum_router


async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_database_connection_pool()
    yield
    await close_database_connection_pool()


app = FastAPI(
    title="Simple headless forum",
    routes=[Mount("/admin/", ADMIN)],
    lifespan=lifespan,
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


@app.get("/", include_in_schema=False)
def index():
    return {"message": "Welcome to Piccolo headless forum"}


app.include_router(router)
app.include_router(forum_router)
