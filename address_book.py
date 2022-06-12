import traceback

from fastapi import APIRouter, Path, Body
from pydantic import BaseModel, Field
from typing import Union, List

from math import sin, cos, sqrt, atan2, radians

from general_db_functions import SQLite3

router = APIRouter()

# approximate radius of earth in km
R = 6373.0

database = SQLite3("address_app.db")   # declaring the database


# pydantic model for the records
class Address(BaseModel):
    name: str = Field(..., description="name of the person to add on to the address book")
    description: str = Field(..., description="description or more info about the place")
    longitude: float = Field(..., description="Enter the longitude of the place (which is one of the co ordinate of the address")
    latitude: float = Field(..., description="Enter the latitude of the place (which is one of the co ordinate of the address")


# pydantic model for the response what we send
class SimpleResponse(BaseModel):
    status: str = Field(..., description="status of the operation")
    message: str = Field(..., description="message for the related operation")


# pydantic model for the validation of the request body of the update end point
class Update(BaseModel):
    longitude: float = Field(...,description="Enter the longitude of the place (which is one of the co ordinate of the address")
    latitude: float = Field(...,description="Enter the latitude of the place (which is one of the co ordinate of the address")



# end point for inserting the address data to database
@router.post("/address/add", response_model=SimpleResponse, summary="insert address of person")
def insertion(req_body: Address):
    try:
        req_json = req_body.dict()
        if database.insert_data("address_book", req_json["name"], req_json["description"], req_json["longitude"], req_json["latitude"]):
            return {"status": "succuss", "message": "inserted successfully"}
        else:
            return {"status": "failed", "message": "insertion failed to database"}
    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "message": "insertion failed to database"}


# updating the records which have the matching name and updating the longitude and latitude
@router.put("/address/update/{name}",response_model=SimpleResponse, summary="update address of person, with his changed location co ordinates")
def updation(name: str = Path(..., title="the name of the person"), req_body: Update = Body(...)):
    try:
        req_json = req_body.dict()
        if database.update_data("address_book", name, req_json["longitude"], req_json["latitude"]):
            return {"status": "succuss", "message": "updated successfully"}
        else:
            return {"status": "failed", "message": f"updation of {name}'s location failed"}
    except Exception as e:
        return {"status": "failed", "message": f"updation of {name}'s location failed"}



# end point for the deletion of the records with matching name of the address
@router.delete("/address/delete/{name}", response_model=SimpleResponse, summary="delete address of person")
def deletion(name:str = Path(..., title="the name of the person to delete")):
    try:
        if database.delete_data("address_book", name):
            return {"status": "succuss", "message": "deleted successfully"}
        else:
            return {"status": "failed", "message": f"deletion of {name}'s address failed"}
    except Exception as e:
        return {"status": "failed", "message": f"deletion of {name}'s address failed"}



# end point for retreving the address which are in the given Kilo Meter range for the giver perticular location co ordinates
@router.get("/address/inrange", response_model=Union[List[Address], SimpleResponse], summary="return list of address with in the distance(in KM) from perticular latitude and longitude")
def inrange(distance: float, latitude: float, longitude: float):
    try:
        data = database.find_data("address_book")
        response = []
        if data:
            for single_address in data:
                lat1 = radians(single_address[3])                # calculations for finding the distance b/w the 2 set of co ordinates
                lon1 = radians(single_address[2])
                lat2 = radians(latitude)
                lon2 = radians(longitude)

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                dist = R * c
                if dist <= distance:          # filtering the matched response
                    response.append({"name": single_address[0], "description": single_address[1], "longitude": single_address[3], "latitude": single_address[2]})
            return response
        else:
            {"status": "failed", "message": f"not able to fetch data"}
    except Exception as e:
        return {"status": "failed", "message": f"not able to fetch data"}



