from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    password: str


class FeaturesModel(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str