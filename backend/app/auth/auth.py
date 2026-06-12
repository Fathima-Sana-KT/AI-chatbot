from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.config import mongo_client
from app.auth import schemas
from app.utils.security import get_password_hash, verify_password, create_access_token

auth_router = APIRouter()
users_collection = mongo_client["ktudb"]["users"]

@auth_router.post("/signup")
async def signup_user(user: schemas.UserCreate):
    try:
        email = user.email.strip().lower()
        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Insert new user
        users_collection.insert_one({
            "name": user.name,
            "email": email,
            "password": get_password_hash(user.password),
            "role": "student"
        })

        return {"message": "User registered successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        print("Signup error:", e)
        raise HTTPException(status_code=500, detail="Signup failed. Try again later.")

@auth_router.post("/login")
async def login_user(user: schemas.UserLogin):
    try:
        email = user.email.strip().lower()
        user_db = users_collection.find_one({"email": email})
        if not user_db or not verify_password(user.password, user_db.get("password")):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": email})
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user": {"email": email, "name": user_db.get("name", "")}
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print("Login error:", e)
        raise HTTPException(status_code=500, detail="Login failed. Try again later.")

