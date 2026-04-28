from fastapi import FastAPI

app = FastAPI(title="Auth Service", version="1.0.0")

@app.get("/api/v1/auth/health")
async def health():
    return {"status": "healthy", "service": "auth"}