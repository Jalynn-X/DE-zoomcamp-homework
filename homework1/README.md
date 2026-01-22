Question 1:
docker run -it --rm --entrypoint=bash python:3.13
then in bash shell: 
pip -V 
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

Question 2:
Answer: db:5432

Question 3:
SELECT count(*)
FROM taxi_trip_201511
WHERE CAST(lpep_pickup_datetime AS DATE) >= '2025-11-01' AND CAST(lpep_pickup_datetime AS DATE) < '2025-12-01'
AND trip_distance<=1;

Answer: 8007

Question 4:
SELECT *
FROM(
	SELECT CAST(lpep_pickup_datetime AS DATE) AS pickup_day, SUM(trip_distance) AS distance
	FROM taxi_trip_201511
	WHERE trip_distance<100
	GROUP BY pickup_day
	)
ORDER BY distance DESC
LIMIT 1;

Answer: 6377

Question 5:
SELECT taxi_zone."Zone"
FROM (
	SELECT "PULocationID", SUM(total_amount) AS amount
	FROM taxi_trip_201511
	WHERE CAST(lpep_pickup_datetime AS DATE) = '2025-11-18'
	GROUP BY "PULocationID"
	ORDER BY amount DESC
	LIMIT 1) taxi
INNER JOIN taxi_zone ON taxi."PULocationID" = taxi_zone."LocationID"

Answer: East Harlem North

Question 6:
SELECT dropoff_zone, SUM(tip_amount) AS tip
FROM (
	SELECT taxi_trip_201511.*, pickup."Zone" AS pickup_zone, dropoff."Zone" AS dropoff_zone
	FROM taxi_trip_201511, taxi_zone pickup, taxi_zone dropoff
	WHERE taxi_trip_201511."PULocationID" = pickup."LocationID"
	AND taxi_trip_201511."PULocationID" = dropoff."LocationID"
	AND pickup."Zone" = 'East Harlem North'
	AND CAST(lpep_pickup_datetime AS DATE) >= '2025-11-01' 
	AND CAST(lpep_pickup_datetime AS DATE) < '2025-12-01') t
GROUP BY dropoff_zone
ORDER BY tip DESC

Answer: East Harlem North




