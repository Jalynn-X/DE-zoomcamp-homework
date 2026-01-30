## Review:
### Question 4:
I should use max for the longest trip distance instead of sum

	SELECT pickup_day
	FROM(
	SELECT CAST(lpep_pickup_datetime AS DATE) AS pickup_day, MAX(trip_distance) AS distance
	FROM taxi_trip_201511
	WHERE trip_distance<100
	GROUP BY pickup_day
		)
	ORDER BY distance DESC
	LIMIT 1;

Correct Answer: 2025-11-14

### Question 6:
I wrote PULocationID for two times and the join condition "PULocationID" = dropoff."LocationID" should be "DOLocationID" = dropoff."LocationID".

	SELECT dropoff_zone, max(tip_amount) AS tip
	FROM (
		SELECT taxi_trip_201511.*, pickup."Zone" AS pickup_zone, dropoff."Zone" AS dropoff_zone
		FROM taxi_trip_201511, taxi_zone pickup, taxi_zone dropoff
		WHERE taxi_trip_201511."PULocationID" = pickup."LocationID"
		AND taxi_trip_201511."DOLocationID" = dropoff."LocationID"
		AND pickup."Zone" = 'East Harlem North'
		AND CAST(lpep_pickup_datetime AS DATE) >= '2025-11-01' 
		AND CAST(lpep_pickup_datetime AS DATE) < '2025-12-01') t
	GROUP BY dropoff_zone
	ORDER BY tip DESC;

Correct Answer:Yorkville West


-------
## Question 1:
Run: 

	docker run -it --rm --entrypoint=bash python:3.13
	pip -V

**answer:**
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

## Question 2:
- **answer:**
  db:5432

## Question 3:
	SELECT count(*)
	FROM taxi_trip_201511
	WHERE CAST(lpep_pickup_datetime AS DATE) >= '2025-11-01'
	AND CAST(lpep_pickup_datetime AS DATE) < '2025-12-01'
	AND trip_distance<=1;

**answer:** 8007

## Question 4:
	SELECT pickup_day
	FROM(
	SELECT CAST(lpep_pickup_datetime AS DATE) AS pickup_day, SUM(trip_distance) AS distance
	FROM taxi_trip_201511
	WHERE trip_distance<100
	GROUP BY pickup_day
		)
	ORDER BY distance DESC
	LIMIT 1;
  
**answer:** 2025-11-20

## Question 5:

	SELECT taxi_zone."Zone"
	FROM (
		SELECT "PULocationID", SUM(total_amount) AS amount
		FROM taxi_trip_201511
		WHERE CAST(lpep_pickup_datetime AS DATE) = '2025-11-18'
		GROUP BY "PULocationID"
		ORDER BY amount DESC
		LIMIT 1) taxi
	INNER JOIN taxi_zone ON taxi."PULocationID" = taxi_zone."LocationID";

**answer:** East Harlem North

## Question 6:
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
	ORDER BY tip DESC;

**answer:** East Harlem North


## TERRAFORM

1. variables.tf

		variable "bq_dataset_name" {
		    description = "bigquery dataset name"
		    default = "demo_dataset"
		}
		
		variable "gcs_bucket_name" {
		    description = "my storage bucket name"
		    default = "project-ebfd82a3-2711-4df0-a4c-terrafrom-bucket"
		}
		
		variable "location" {
		    description = "location of project"
		    default = "europe-west1"
		}
		
		variable "project" {
		    description = "project"
		    default = "project-ebfd82a3-2711-4df0-a4c"
		}

2. main.tf

		terraform {
		  required_providers {
		    google = {
		      source  = "hashicorp/google"
		      version = "7.16.0"
		    }
		  }
		}
		
		provider "google" {
		  project = var.project
		  region  = var.location
		}
		
		resource "google_storage_bucket" "terraform-demo" {
		  name                        = var.gcs_bucket_name
		  location                    = var.location
		  force_destroy               = true
		  uniform_bucket_level_access = true
		
		  lifecycle_rule {
		    condition {
		      age = 1
		    }
		    action {
		      type = "AbortIncompleteMultipartUpload"
		    }
		  }
		}
		
		resource "google_bigquery_dataset" "demo-dataset" {
		  dataset_id = var.bq_dataset_name
		  location = var.location
		  delete_contents_on_destroy = true
		}
	
	## Question 7:
	**answer:** terraform init, terraform apply -auto-approve, terraform destroy
