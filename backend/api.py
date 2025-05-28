from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from models import UserModel, FeaturesModel
from repositories import UserRepository
from sqlalchemy.orm import Session
from database import Get_db
from entities import User
from security import SecurityManager, EndpointVerification
import uvicorn
from housing_prices_dashboard.main import load_model
import numpy as np
from ml_utils import map_dummy_variable
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


app =FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
mlModel = load_model(r'C:\Users\richard.macus\Desktop\housing_prices_app\housing_prices_dashboard\model.joblib')


@app.post("/registration")
def Registration(user: UserModel,
                 dbConnection: Session = Depends(Get_db)):

    userRepo = UserRepository(dbConnection)
    existingUser = userRepo.GetUserByName(user.username)

    if existingUser is not None:
        raise HTTPException(status_code=409,
                            detail="Username already exists")

    hashedPassword = SecurityManager.HashPassword(user.password)
    newUser = User(username = user.username,
                   password = hashedPassword)
    addedUser = userRepo.CreateUser(newUser)

    return JSONResponse(status_code=201,
                        content={"message": "User created successfully",
                                 "user": addedUser.as_dict() ,},)


@app.post("/login")
def Login(user: UserModel,
          dbConnection: Session = Depends(Get_db)):

    userRepo = UserRepository(dbConnection)
    securityManager = SecurityManager()
    existingUser:User = userRepo.GetUserByName(user.username)

    if existingUser is None:
        raise HTTPException(status_code=401,
                            detail="User does not exist")

    hashedPassword = existingUser.password
    validPassword = securityManager.VerifyPassword(user.password,
                                                   hashedPassword)

    if not validPassword:
        raise HTTPException(status_code=401,
                            detail="Invalid password")

    token = securityManager.CreateJWTToken({"name":user.username,
                                            "password":user.password})
    return JSONResponse(status_code=200,content={"access_token": token,
                                                 "token_type": "bearer"})


@app.post("/predict")
@limiter.limit("10/minute")
def Predict(request: Request,
            features:FeaturesModel,
            jwtTokenPayload:dict = Depends(EndpointVerification)):

    dummy_values = map_dummy_variable(features.ocean_proximity)
    input_array = [features.longitude,
                    features.latitude,
                    features.housing_median_age,
                    features.total_rooms,
                    features.total_bedrooms,
                    features.population,
                    features.households,
                    features.median_income]+dummy_values
    input_array_np = np.array(input_array).reshape(1, -1)
    prediction = mlModel.predict(input_array_np)
    return JSONResponse(status_code=200,
                        content={"price":prediction[0]})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)