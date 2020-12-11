import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.serializers import create_pydantic_model
from pydantic import BaseModel


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: t.Optional[str] = None


# user schema
UserModelIn = create_pydantic_model(
    table=BaseUser,
    model_name="UserModelIn",
)
UserModelOut = create_pydantic_model(
    table=BaseUser,
    include_default_columns=True,
    model_name="UserModelOut",
)
