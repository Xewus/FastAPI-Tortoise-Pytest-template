from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from src.config import TORTOISE_CONFIG, Urls, app_settings
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    debug=app_settings.debug,
    title=app_settings.app_title,
    version=app_settings.app_version,
    description=app_settings.app_description,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

register_tortoise(app=app, **TORTOISE_CONFIG)


@app.get(path="/", deprecated=True)
async def index(req: Request):
    return RedirectResponse(str(req.base_url) + "docs")
