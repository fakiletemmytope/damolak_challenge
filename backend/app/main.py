from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, init_db
from app.routers import admin, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized")
    yield
    try:
        await engine.dispose()
    except Exception as e:
        print(f"Error disposing database engine: {e}")
    finally:
        await engine.dispose()
        print("Database engine disposed")


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(admin.router, tags=["admin"])


@app.get("/health")
async def health():
    return {"status": "healthy"}
