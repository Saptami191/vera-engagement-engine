from fastapi import FastAPI
from app.api.routes import meta, context, tick, reply
from app.state.store import init_db
from app.core.config import settings
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Deterministic AI Engagement Engine for Vera"
)

# Include Routers
app.include_router(meta.router, prefix=settings.API_V1_STR)
app.include_router(context.router, prefix=settings.API_V1_STR)
app.include_router(tick.router, prefix=settings.API_V1_STR)
app.include_router(reply.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
