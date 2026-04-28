from fastapi import FastAPI

app = FastAPI(title="Analytics Service", version="1.0.0")

@app.get("/api/v1/analytics/health")
async def health():
    return {"status": "healthy", "service": "analytics"}