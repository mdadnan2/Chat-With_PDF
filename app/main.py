from fastapi import FastAPI
from app.config import settings
from app.routers.upload import router as upload_router
from app.routers.chat import router as chat_router



app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(upload_router, prefix="/api/v1")
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.app_name}!"}




