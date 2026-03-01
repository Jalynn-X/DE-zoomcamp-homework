"""Template for building a `dlt` pipeline to ingest data from a REST API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig
import requests

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

# Define the REST API resource
@dlt.resource(name="nyc_taxi_data")
def nyc_taxi_data():
    page = 1
    while True:
        # Request the current page
        response = requests.get(BASE_URL, params={"page": page})
        response.raise_for_status()
        data = response.json()

        # Stop when API returns empty list
        if not data:
            break

        yield data
        page += 1

# Wrap the resource as a source
@dlt.source
def taxi_pipeline_rest_api_source():
    return nyc_taxi_data()


# Define the pipeline
pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",  # matches your homework
    destination="duckdb",
    dataset_name="taxi_data",
    refresh="drop_sources",  # cleans data/state on each run
    progress="log",  # shows progress
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)