# Assignment4
# Streamlit-S3 Integration using FastAPI
This project demonstrates the integration of Streamlit with Amazon S3 using FastAPI. It provides endpoints to upload files to an S3 bucket and retrieve data from Snowflake.

## Prerequisites
Before running the application, ensure you have the following installed:

Python 3.9 or higher
Docker (optional, for containerization)

## Setup
1. Clone the repository to your local machine:

``` bash
git clone [<repository_url>](https://github.com/BigDataIA-Spring2024-Sec2-Team4/Assignment4)
cd Assignment4
```

3. Install dependencies:

``` bash
pip install -r requirements.txt
```

6. Set up your AWS credentials and Snowflake credentials by creating a .env file in the root directory and adding the following variables:
``` bash
# AWS credentials
AWS_REGION=<your_aws_region>
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
BUCKET_NAME=<your_bucket_name>

# Snowflake credentials
SNOWFLAKE_ACCOUNT=<your_snowflake_account>
SNOWFLAKE_USER=<your_snowflake_user>
SNOWFLAKE_PASSWORD=<your_snowflake_password>
SNOWFLAKE_DATABASE=<your_snowflake_database>
SNOWFLAKE_SCHEMA=<your_snowflake_schema>
SNOWFLAKE_WAREHOUSE=<your_snowflake_warehouse>
SNOWFLAKE_TABLE=<your_snowflake_table>
```

## Usage
## 1. Running the FastAPI Server
Start the FastAPI server by running the following command:
``` bash
uvicorn app:app --reload
```

## 2. Uploading Files to S3
To upload a file to the configured S3 bucket, make a POST request to the /upload endpoint with the file attached as form data.

Example using curl:

``` bash
curl -X POST -F "file=@/path/to/your/file.txt" http://localhost:8000/upload
```

## 3. Fetching Data from Snowflake
To retrieve data from Snowflake, make a GET request to the /get_data endpoint.
Example using curl:
``` bash
curl http://localhost:8000/get_data
```

## Docker Support
You can also run the application using Docker. Use the provided Dockerfile and docker-compose.yml files to build and run the containers.

Build the Docker image:

``` bash
docker build -t streamlit-s3 .
```

Run the Docker container:

``` bash
docker run -d -p 8000:8000 streamlit-s3
```

