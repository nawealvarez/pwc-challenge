from app.middlewares.correlation import CorrelationIDMiddleware
from app.middlewares.cors import get_cors_config
from app.middlewares.rate_limit import RateLimitMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import api_versions

app = FastAPI(title="Course API", version="1.0.0")

app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(CORSMiddleware, **get_cors_config())
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

Base.metadata.create_all(bind=engine)

for version, router in api_versions.items():
    app.include_router(router)


@app.get("/health", tags=["Meta"])
def health():
  return {"status": "ok"}

@app.get("/version", tags=["Meta"])
def version():
  return {"version": app.version}