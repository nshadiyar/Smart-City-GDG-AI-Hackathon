from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.poi import router as poi_router
from app.routers.recommend import router as recommend_router


app = FastAPI(title="RAG Walks Astana", version="0.1.0")

# CORS for local dev (Next.js on 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    # Lazy initialize services on import of routers
    return


app.include_router(health_router, prefix="/api")
app.include_router(poi_router, prefix="/api")
app.include_router(recommend_router, prefix="/api")
