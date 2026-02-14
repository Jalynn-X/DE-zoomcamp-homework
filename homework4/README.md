## DBT homework

## Question 3:
Query:
````sql
select count(*) from {{ ref('fct_monthly_zone_revenue') }}
````

Answer: 12,184

## Question 4:
Query:
````sql
select *
from  {{ ref('fct_monthly_zone_revenue') }}
where service_type = 'Green'
order by revenue_monthly_total_amount desc
limit 1
````
Answer: East Harlem North

## Question 5:
Query:
````sql
select revenue_month, sum(total_monthly_trips)
from {{ ref('fct_monthly_zone_revenue') }}
where service_type = 'Green' and revenue_month = '2019-10-01'
group by revenue_month
````
Answer: 384,624

## Question 6:
Query:
````sql
select revenue_month, sum(total_monthly_trips)
from {{ ref('fct_monthly_zone_revenue') }}
where service_type = 'Green' and revenue_month = '2019-10-01'
group by revenue_month

with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers
        cast(dispatching_base_num as varchar) as dispatching_base_number,
        cast(Affiliated_base_number as varchar) as affiliated_base_number,

        -- timestamps
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropoff_datetime,

        -- trip info
        cast(PUlocationID as integer) as pickup_location_id,
        cast(DOlocationID as integer) as dropoff_location_id,
        cast(SR_Flag as integer) as sr_flag

    from source
    -- Filter out records with null vendor_id (data quality requirement)
    where dispatching_base_num is not null
)

select count(*) from renamed
````
Answer: 43,244,693
