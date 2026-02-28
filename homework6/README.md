## Spark homework

## Question 1:
````python
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
spark.version
````

Answer: '3.5.3'

## Question 2:
Query:
````python
select *
from  {{ ref('fct_monthly_zone_revenue') }}
where service_type = 'Green'
order by revenue_monthly_total_amount desc
limit 1

# then use bash:
$ du -h hw/yellow/nov/*
0       hw/yellow/nov/_SUCCESS
25M     hw/yellow/nov/part-00000-08f950c7-594a-4cf1-a246-08c1d1837c25-c000.snappy.parquet
25M     hw/yellow/nov/part-00001-08f950c7-594a-4cf1-a246-08c1d1837c25-c000.snappy.parquet
25M     hw/yellow/nov/part-00002-08f950c7-594a-4cf1-a246-08c1d1837c25-c000.snappy.parquet
25M     hw/yellow/nov/part-00003-08f950c7-594a-4cf1-a246-08c1d1837c25-c000.snappy.parquet
````
Answer: 25M

## Question 3:
Query:
````python
df_yellow_count = spark.sql("""
SELECT 
    COUNT(1) AS number_records
FROM
    yellow_nov
WHERE
    tpep_pickup_datetime >= '2025-11-15 00:00:00'
AND
    tpep_pickup_datetime < '2025-11-16 00:00:00'
""")

df_yellow_count.show()
````
Answer: 162,604

## Question 4:
Query:
````python
df_yellow_hours = spark.sql("""
SELECT 
    (unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600 AS diff_hour 
FROM
    yellow_nov
ORDER BY
    diff_hour DESC
LIMIT 1
""")

df_yellow_hours.show()
````
Answer: 90.6

## Question 6:
Query:
````python
df_join = df_yellow_nov.join(df_timezone, df_yellow_nov.PULocationID == df_timezone.LocationID, how='inner')
df_join.registerTempTable('join_temp')
df_least_pickup_zone = spark.sql("""
SELECT
    Zone,
    COUNT(*) AS number_records
FROM
    join_temp
GROUP BY
    Zone
ORDER BY
    number_records ASC
""")

df_least_pickup_zone.show()
````
Answer: Governor's Island/Ellis Island/Liberty Island
