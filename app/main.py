from fastapi import FastAPI, Request, status
from app.models.models import Base
from app.database.database import engine
from app.api import analytics, barcode, qrcode, shorturl, metadata, auth, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from sqlalchemy.exc import OperationalError

app = FastAPI()

# Create tables on startup, but don't crash the server if DB is down
@app.on_event("startup")
async def startup_db():
	try:
		Base.metadata.create_all(bind=engine)
	except OperationalError as e:
		# Log a concise warning; endpoints that hit DB will still raise 500 until DB is up
		print("[Startup] Database not available; will retry on first DB access.")

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(analytics.router)
app.include_router(barcode.router)
app.include_router(qrcode.router)
app.include_router(shorturl.router)
app.include_router(metadata.router)
app.include_router(auth.router)
app.include_router(users.router)

print("GOOGLE_CLIENT_ID:", settings.google_client_id)
