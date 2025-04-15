from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import api_versions

app = FastAPI(title="Course API", version="1.0.0")

Base.metadata.create_all(bind=engine)

for version, router in api_versions.items():
    app.include_router(router)


@app.get("/health", tags=["Meta"])
def health():
  return {"status": "ok"}

@app.get("/version", tags=["Meta"])
def version():
  return {"version": app.version}