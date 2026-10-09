import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-8dcn3z.example.com"
EMAIL = "24f2005600@ds.study.iitm.ac.in"

# CORS: only this one origin gets the ACAO header (no "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Added AFTER the CORS middleware, so it wraps it and also stamps preflight responses
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/stats")
def stats(values: str = ""):
    nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]
    if not nums:
        return {"email": EMAIL, "count": 0, "sum": 0, "min": None, "max": None, "mean": 0}
    total = sum(nums)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }
