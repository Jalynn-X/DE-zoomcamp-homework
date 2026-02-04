## BigQuery Setup
Create external table: 

````sql
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-486015.zoomcamp.external_yellow_tripdata
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-bucket-zoomcamp-jalynn/yellow_tripdata_2024-*.parquet']
);
````

Create materialized non-partitioned table:
````sql
CREATE OR REPLACE TABLE `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`
AS SELECT * FROM `de-zoomcamp-486015.zoomcamp.external_yellow_tripdata`;
````

## Question 1:
Query:
````sql
SELECT COUNT(*) FROM `de-zoomcamp-486015.zoomcamp.external_yellow_tripdata`;
````
Answer: 20332093

## Question 2:
Query:
````sql
SELECT DISTINCT COUNT(PULocationID) FROM `de-zoomcamp-486015.zoomcamp.external_yellow_tripdata`;
SELECT DISTINCT COUNT(PULocationID) FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`;
````
Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

## Question 3:
Query:
````sql
SELECT PULocationID FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`;
SELECT PULocationID,DOLocationID FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`;
````
Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

## Question 4:
Query:
````sql
SELECT COUNT(fare_amount) FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata` WHERE fare_amount = 0;
````
Answer: 8333

## Question 5:
Query:
````sql
CREATE OR REPLACE TABLE `de-zoomcamp-486015.zoomcamp.yellow_partitioned_tripdata`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS (
  SELECT * FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`
);
````
Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

## Question 6:
Query:
````sql
SELECT DISTINCT VendorID
FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `de-zoomcamp-486015.zoomcamp.yellow_partitioned_tripdata`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
````
Answer:310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

## Question 9:
Query:
````sql
SELECT COUNT(*) FROM `de-zoomcamp-486015.zoomcamp.yellow_nonpartitioned_tripdata`;
````
Answer: Estimation is 0B. BigQuery stores row counts in metadata for each storage block of a table.For a plain COUNT(*) (without any filters, no column references), it doesn’t need to read any actual column data.
