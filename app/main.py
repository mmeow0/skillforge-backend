# app/main.py
from fastapi import FastAPI
from app.api import auth_routes, course_routes, user_routes
from app.core.config import configure_cors

app = FastAPI()

# Configure CORS settings
configure_cors(app)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(course_routes.router, prefix="/courses", tags=["courses"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Clean Architecture project!"}
