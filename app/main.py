from fastapi import FastAPI, Request, status
from app.db.init_db import Base
from app.db.session import engine
from app.api import analytics, barcode, qrcode, shorturl, metadata, auth, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.celery_app import create_celery

app = FastAPI()

Base.metadata.create_all(bind=engine) 

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(analytics.router)
app.include_router(barcode.router)
app.include_router(qrcode.router)
app.include_router(shorturl.router)
app.include_router(metadata.router)
app.include_router(auth.router)
app.include_router(users.router)

# Initialize Celery app (keeps config in one place; workers can import `app.celery_app`)
celery = create_celery()

print("GOOGLE_CLIENT_ID:", settings.google_client_id)
