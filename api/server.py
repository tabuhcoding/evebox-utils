import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from depends import get_routers


class Server:
    api_handler: FastAPI

    def __init__(self):
        self.api_handler = FastAPI(docs_url="/swagger/index.html")
        self.api_handler.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Include all routers
        for _, router in enumerate(get_routers()):
            self.api_handler.include_router(router)

    def run(self):
        uvicorn.run(
            self.api_handler,
            host='0.0.0.0',
            port=8000,
            log_level="debug",
            proxy_headers=True,
        )
