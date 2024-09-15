from fastapi import APIRouter
from ..utils.auth import get_connection
from app.schemas import Cube, FeatureCollection
from rasterio.io import MemoryFile

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
    fc = aoi.to_geojson()
    print(type(fc))
    if fc.is_valid:
        return {"aoi": aoi, "geojson": fc}
    else:
        return {"error": "Invalid GeoJSON"} 


@router.post("/openeo/process/timeseries")
async def time_series(data: Cube, aoi: FeatureCollection):
    conn = get_connection()
    datacube = conn.load_collection(
        collection_id=data.collection_id,
        temporal_extent=data.temporal_extent,
        bands=data.bands
    )

    red = datacube.band('B04')
    nir = datacube.band('B08')
    ndvi = (nir - red) / (nir + red)


    fc = aoi.to_geojson()
    ts = ndvi.aggregate_spatial(geometries=fc, reducer='mean')
    result = ts.execute()

    time_series_data = []
    for date, value in result.items():
        ndvi_values = [v[0] for v in value]
        time_series_data.append({
            "date": date,
            "ndvi": ndvi_values
        })

    return {"time_series": time_series_data}



@router.post("/openeo/process/image")
async def process_image(data: Cube, aoi: FeatureCollection):
    conn = get_connection()
    datacube = conn.load_collection(
        collection_id=data.collection_id,
        temporal_extent=data.temporal_extent,
        bands=data.bands
    )

    fc = aoi.to_geojson()
    clipped_cube = datacube.filter_spatial(geometries=fc)
    
    with MemoryFile(clipped_cube.download()) as memfile:
        with memfile.open() as dataset:
            
            print(type(dataset), dataset.shape, dataset.count, dataset.bounds, dataset.crs)
            return {"data": dataset.read(1).tolist()}