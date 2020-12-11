from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper
from starlette.routing import Mount, Route

from accounts.endpoints import oauth2_scheme, router
from forum.tables import Category, Reply, Topic
from home.endpoints import HomeEndpoint

app = FastAPI(
    title="Simple headless forum",
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=[Category, Reply, Topic],
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
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

FastAPIWrapper(
    root_url="/categories/",
    fastapi_app=app,
    piccolo_crud=PiccoloCRUD(
        table=Category,
        read_only=False,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["Category"]},
        post={"dependencies": [Depends(oauth2_scheme)]},
        put={"dependencies": [Depends(oauth2_scheme)]},
        patch={"dependencies": [Depends(oauth2_scheme)]},
        delete_single={"dependencies": [Depends(oauth2_scheme)]},
    ),
)

FastAPIWrapper(
    root_url="/topics/",
    fastapi_app=app,
    piccolo_crud=PiccoloCRUD(
        table=Topic,
        read_only=False,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["Topics"]},
        post={"dependencies": [Depends(oauth2_scheme)]},
        put={"dependencies": [Depends(oauth2_scheme)]},
        patch={"dependencies": [Depends(oauth2_scheme)]},
        delete_single={"dependencies": [Depends(oauth2_scheme)]},
    ),
)

FastAPIWrapper(
    root_url="/replies/",
    fastapi_app=app,
    piccolo_crud=PiccoloCRUD(
        table=Reply,
        read_only=False,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["Replies"]},
        post={"dependencies": [Depends(oauth2_scheme)]},
        put={"dependencies": [Depends(oauth2_scheme)]},
        patch={"dependencies": [Depends(oauth2_scheme)]},
        delete_single={"dependencies": [Depends(oauth2_scheme)]},
    ),
)


@app.on_event("startup")
async def open_database_connection_pool():
    engine = engine_finder()
    await engine.start_connnection_pool()


@app.on_event("shutdown")
async def close_database_connection_pool():
    engine = engine_finder()
    await engine.close_connnection_pool()
