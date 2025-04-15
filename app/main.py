from fastapi import FastAPI

app = FastAPI(title="Course API", version="1.0.0")

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.get("/health", tags=["Meta"])
def health():
  return {"status": "ok"}

@app.get("/version", tags=["Meta"])
def version():
  return {"version": app.version}