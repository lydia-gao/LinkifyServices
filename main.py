from fastapi import FastAPI, Request, status
from models import Base
from database import engine
from routers import analytics, barcode, qrcode, shorturl, metadata
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from config import settings

app = FastAPI()

Base.metadata.create_all(bind=engine) 

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(analytics.router)
app.include_router(barcode.router)
app.include_router(qrcode.router)
app.include_router(shorturl.router)
app.include_router(metadata.router)

print("GOOGLE_CLIENT_ID:", settings.google_client_id)
