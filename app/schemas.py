from pydantic import BaseModel
import geojson


class Credentials(BaseModel):
    client_id: str
    client_secret: str


class Cube(BaseModel):
    collection_id: str
    temporal_extent: list
    bands: list


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
    