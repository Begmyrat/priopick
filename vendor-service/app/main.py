from fastapi import FastAPI

app = FastAPI(title="Vendor Service", version="1.0.0")

@app.get("/api/v1/vendors/health")
async def health():
    return {"status": "healthy", "service": "vendor"}