from fastapi import FastAPI

app = FastAPI(title="Planner Service", version="1.0.0")

@app.get("/api/v1/plans/health")
async def health():
    return {"status": "healthy", "service": "planner"}