import os
from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import analytics, barcode, history, qrcode, shorturl
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


app.include_router(analytics.router)
app.include_router(barcode.router)
app.include_router(history.router)
app.include_router(qrcode.router)
app.include_router(shorturl.router)
app.include_router(shorturl.router)

print("GOOGLE_CLIENT_ID:", os.getenv("GOOGLE_CLIENT_ID"))
