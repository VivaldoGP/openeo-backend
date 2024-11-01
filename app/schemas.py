from pydantic import BaseModel, EmailStr
import geojson



class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class Credentials(BaseModel):
    client_id: str
    client_secret: str


class Cube(BaseModel):
    collection_id: str
    temporal_extent: list
    bands: list = ['B04', 'B08']


class Feature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict

class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[Feature]

    def to_geojson(self):
        
        fc = geojson.dumps(self.model_dump())
        return geojson.loads(fc)
    
class TimeSeriesFormDate(BaseModel):
    cube: Cube
    aoi: FeatureCollection