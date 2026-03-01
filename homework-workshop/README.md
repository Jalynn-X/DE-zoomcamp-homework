## Spark homework

## Question 1:
````sql
SELECT MIN(trip_pickup_date_time), MAX(trip_dropoff_date_time) FROM taxi_data.nyc_taxi_data
````

Answer: 2009-06-01 to 2009-07-01

## Question 2:
Query:
````sql
SELECT COUNT(1) FILTER (WHERE payment_type = 'Credit') / COUNT(1) * 100 AS percent 
FROM taxi_data.nyc_taxi_data
````
Answer: 26.66

## Question 3:
Query:
````sql
SELECT ROUND(SUM(tip_amt),2) FROM taxi_data.nyc_taxi_data
````
Answer: 6,063.41
