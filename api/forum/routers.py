from fastapi import APIRouter, Depends
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from api.accounts.routers import oauth2_scheme
from api.forum.tables import Category, Reply, Topic

forum_router = APIRouter()


FastAPIWrapper(
    root_url="/categories/",
    fastapi_app=forum_router,
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
    fastapi_app=forum_router,
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
    fastapi_app=forum_router,
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
