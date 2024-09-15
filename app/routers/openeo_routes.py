from fastapi import APIRouter
from ..utils.auth import get_connection
from app.schemas import Cube, FeatureCollection
import geojson

router = APIRouter()

@router.get("/openeo/available_collections")
async def available_collections():
    conn = get_connection()
    collections = conn.list_collections()
    return {"collections": collections}


@router.get("/openeo/collection")
async def get_collection(collection_id: str):
    conn = get_connection()
    collection = conn.describe_collection(collection_id=collection_id)
    return collection


@router.post("/openeo/check_aoi")
async def check_aoi(aoi: FeatureCollection):
    fc = geojson.dumps(aoi.model_dump())
    print(fc)
    return {"aoi": aoi, "geojson": geojson.loads(fc)}


@router.post("/openeo/process/timeseries")
async def time_series(data: Cube, aoi: FeatureCollection):
    print(aoi)
    conn = get_connection()
    datacube = conn.load_collection(
        collection_id=data.collection_id,
        temporal_extent=data.temporal_extent,
        bands=data.bands
    )

    red = datacube.band('B04')
    nir = datacube.band('B08')
    ndvi = (nir - red) / (nir + red)


    fc = geojson.dumps(aoi.model_dump())
    ts = ndvi.aggregate_spatial(geometries=geojson.loads(fc), reducer='mean')
    result = ts.execute()

    dates = list(result.keys())
    values_by_date = [list(map(lambda x: x[0], result[date])) for date in dates]

    ndvi_cols = list(map(list, zip(*values_by_date)))

    formatted_result = {
        "dates": dates,
    }

    for i, column in enumerate(ndvi_cols, start=1):
        formatted_result[f"ndvi_{i}"] = column

    return formatted_result
