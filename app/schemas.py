from pydantic import BaseModel


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