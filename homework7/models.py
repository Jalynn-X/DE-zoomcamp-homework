import json
from dataclasses import dataclass
import pandas as pd

@dataclass
class Ride:
    lpep_pickup_datetime: str
    lpep_dropoff_datetime: str
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float

def ride_from_row(row):
    return Ride(
        lpep_pickup_datetime=str(row["lpep_pickup_datetime"]),
        lpep_dropoff_datetime=str(row["lpep_dropoff_datetime"]),
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        passenger_count=int(row["passenger_count"]) if not pd.isna(row["passenger_count"]) else 0,
        trip_distance=float(row['trip_distance']) if not pd.isna(row["trip_distance"]) else 0.0,
        tip_amount=float(row["tip_amount"]) if not pd.isna(row["tip_amount"]) else 0.0,
        total_amount=float(row['total_amount']) if not pd.isna(row["total_amount"]) else 0.0,
    )

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
