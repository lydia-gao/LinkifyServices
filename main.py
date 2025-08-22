from fastapi import FastAPI, Request, status
from models import Base
from database import engine
from routers import analytics, barcode, history, qrcode, url
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from config import settings   # 👈 统一用 config.py

app = FastAPI()

# Base.metadata.create_all(bind=engine)  # 一般在 Alembic 迁移里做，不推荐在 app 启动时自动建表

# 用 config.py 中的 SECRET_KEY
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# 挂载路由
app.include_router(analytics.router)
app.include_router(barcode.router)
app.include_router(qrcode.router)
app.include_router(url.router)

# 用 config.py 中的 GOOGLE_CLIENT_ID
print("GOOGLE_CLIENT_ID:", settings.google_client_id)
