from fastapi import FastAPI
import openeo
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import os


class Cube(BaseModel):
    collection_id: str
    temporal_extent: list
    bands: list


fields = json.loads(
    """{
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[5.055945487931457, 51.222709834076504], [5.064972484168688, 51.221122565090525], [5.064972484168688, 51.221122565090525], [5.067474954083448, 51.218249806779134], [5.064827929485983, 51.21689628072789], [5.05917785594747, 51.217191909908095], [5.053553857094518, 51.21807492332223], [5.055945487931457, 51.222709834076504]]]}}, 
        {"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[5.063345886679116, 51.23087606640057], [5.06604742694687, 51.22886710731809], [5.070627820472246, 51.22874440121892], [5.068403609708207, 51.22657208381529], [5.064823257492447, 51.22676051738515], [5.064892324615199, 51.2283032878514], [5.063641745941974, 51.2285757299238], [5.062340811262595, 51.227722351687945], [5.06076005158084, 51.228042312276536], [5.063345886679116, 51.23087606640057]]]}},
        {"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[5.07163184674986, 51.23481147556147], [5.076706025697324, 51.23317590781036], [5.077828303041866, 51.233226237184724], [5.078024733866917, 51.23263978271262], [5.080771081607657, 51.23259097170763], [5.083734842574312, 51.23530464074437], [5.080957826735458, 51.23646091560258], [5.079752631651647, 51.23519531038643], [5.077238400183506, 51.23490534677628], [5.072856439300575, 51.23593546777778], [5.07163184674986, 51.23481147556147]]]}}, 
        {"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[5.083897244679042, 51.23510639883143], [5.081302408741335, 51.232922477780846], [5.082963802194108, 51.233146058575876], [5.084497702305552, 51.232672717580655], [5.085732850338428, 51.2340852086282], [5.083897244679042, 51.23510639883143]]]}}
    ]}
"""
)


def get_connection():
    load_dotenv()
    user = os.getenv("Client_ID")
    password = os.getenv("Client_secret")
    connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
    conn = connection.authenticate_oidc_client_credentials(
        client_id=user,
        client_secret=password
    )
    return conn


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/openeo/process')
async def process_data(data: Cube):
    conn = get_connection()
    datacube = conn.load_collection(
        collection_id=data.collection_id,
        temporal_extent=data.temporal_extent,
        bands=data.bands
    )

    red = datacube.band('B04')
    nir = datacube.band('B08')
    ndvi = (nir - red) / (nir + red)

    ts = ndvi.aggregate_spatial(geometries=fields, reducer='mean')
    result = ts.execute()

    flattened_result = {
        date: [value[0] for value in values]
        for date, values in result.items()
    }

    # Devolver los resultados como JSON con listas aplanadas
    return flattened_result

