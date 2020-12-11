from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse


class HomeEndpoint(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(
            {
                "message": "Welcome to Piccolo headless forum",
            }
        )
