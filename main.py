from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine

# 1. First, import your database models completely
import models 

# 2. Next, import your routes
from routes import auth, inventory
import traceback

# 3. Now create the tables (Since models is imported above, SQLAlchemy WILL see the users table!)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    description="A secure RESTful API for retail inventory tracking system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handling middleware to print clean debug info
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print("\n🔥 SERVER ERROR DETECTED:\n")
        traceback.print_exc()
        return PlainTextResponse(f"Internal Server Error: {str(e)}", status_code=500)

# Include Routers
app.include_router(auth.router)
app.include_router(inventory.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Inventory Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }