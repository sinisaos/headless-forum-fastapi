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
UserModelIn: t.Any = create_pydantic_model(
    table=BaseUser,
    exclude_columns=(
        BaseUser.first_name,
        BaseUser.last_name,
        BaseUser.admin,
        BaseUser.superuser,
        BaseUser.last_login,
    ),
    model_name="UserModelIn",
)
UserModelOut: t.Any = create_pydantic_model(
    table=BaseUser,
    include_default_columns=True,
    model_name="UserModelOut",
)
