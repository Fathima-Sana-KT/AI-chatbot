from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.config import mongo_client

auth_router = APIRouter()
users_collection = mongo_client["ktudb"]["users"]

@auth_router.post("/signup")
async def signup_user(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "student")  # default role

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return JSONResponse(status_code=400, content={"message": "User already exists"})

        # Insert new user
        users_collection.insert_one({
            "email": email,
            "password": password,
            "role": role
        })

        return JSONResponse(status_code=201, content={"message": "User registered successfully"})

    except Exception as e:
        print("Signup error:", e)
        return JSONResponse(status_code=500, content={"message": "Signup failed. Try again later."})
