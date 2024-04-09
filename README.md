# Assignment4
## Live application Links


[![codelabs](https://img.shields.io/badge/codelabs-4285F4?style=for-the-badge&logo=codelabs&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=15TX801JmThAB60DlI9FU_bpRoIJUoFUyyn1WPdTcb7M#0)

## Problem Statement
The aim is to automate PDF data extraction and storage into Snowflake using Airflow and FastAPI. Streamlit serves as the user interface for PDF upload and triggering the pipeline. Dockerize services and host online for seamless integration.

## Project Goals
The task involves building an end-to-end pipeline utilizing Airflow for automating the extraction and storage of meta-data and content from PDF files into Snowflake. This requires the development of two API services using FastAPI. The first API service will trigger an Airflow pipeline upon receiving the S3-file location, facilitating extraction, data validation, and loading of data and metadata into Snowflake. The second API service will interact with Snowflake to execute queries and return responses. Additionally, the Streamlit framework will serve as the interface for the end-user application to upload PDF files, initiate the pipeline, and display the results obtained from Snowflake.

## Architecture Diagram
<img width="789" alt="Architecture_Diagram" src="https://github.com/BigDataIA-Spring2024-Sec2-Team4/Assignment4/assets/144851281/b043031b-0040-4db4-a688-9623be0272ce">

## Technologies Used
- Airflow
- FastAPI
- Snowflake
- Streamlit
- Docker
- AWS S3

## Data Sources



# Streamlit-S3 Integration using FastAPI
This project demonstrates the integration of Streamlit with Amazon S3 using FastAPI. It provides endpoints to upload files to an S3 bucket and retrieve data from Snowflake.

## Prerequisites
Before running the application, ensure you have the following installed:

- Python 3.9 or higher
- Docker (optional, for containerization)
- Snowflake account setpu
- AWS Account setup and an S3 bucket

## Project Structure
```⁠ bash

.gitignore
requirements.txt
LICENSE
README
DBT-Snowflake.txt
Datasets
airflow_app
   |--architectural_diagram
   |  |--Architectural Diagram.ipynb
   |  |--Streamlit.png
   |  |--airflow.png
   |  |--fastAPI.png
   |--dags
   |  |--_init_.py
   |  |--consolidated_dag.py
   |--src
   |  |--PdfExtraction
   |  |--dataset
   |  |--dbt_proj
   |  |--pydantic_project
   |  |--scrapy
   |  |--DBT-Snowflake.sql
   |  |--_init_.py
   |  |--.env
   |  |--Dockerfile
   |  |--docker-compose.yaml
streamlit_app
   |-- pages
   |  |-- extraction.py
   |  |-- streamlit_app.py
fastapi
   |-- uploadend.api
   |-- display.api


```

## Setup
1. Clone the repository to your local machine:

```bash
git clone [Assignment4 GitHub repository](https://github.com/BigDataIA-Spring2024-Sec2-Team4/Assignment4)
cd Assignment4
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Set up your AWS credentials and Snowflake credentials by creating a .env file in the root directory and adding the following variables:
```bash
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
docker build -t streamlit_app-s3 .
```

Run the Docker container:

``` bash
docker run -d -p 8000:8000 streamlit_app-s3
```

## Learning Outcomes
- Understanding of orchestrating data pipelines using Airflow.
- Proficiency in building API services using FastAPI for seamless interaction with other systems.
- Hands-on experience with cloud data warehouses like Snowflake for storing and querying data.
- Familiarity with Streamlit framework for developing user-friendly interfaces.
- Knowledge of Docker for containerizing applications and facilitating easy deployment.
- Experience in hosting services online for accessibility and scalability.
- Enhanced skills in handling PDF data extraction and processing in a distributed environment.
- Ability to design and implement end-to-end data solutions for real-world applications.


## Conclusion
The project successfully implements an automated pipeline for handling PDF data extraction and storage into Snowflake. By utilizing Airflow for orchestration and FastAPI for building API services, alongside Streamlit for user interaction, the solution ensures efficient data handling and accessibility. Dockerization of the Streamlit app and API services enables easy deployment and scalability, while hosting these services online ensures accessibility from anywhere. Overall, the implemented architecture streamlines the process of handling PDF data, enhancing efficiency and accessibility for users.

## Team Information and Contribution

| Name       | Contribution % | Contributions                             |
|------------|----------------|-------------------------------------------|
| Riya Singh  |      32       | Created Dag in Airflow, worked on the tasks in airflow, Data Extraction using PyPDF2, Data Validation using Pydantic, Architectural Diagram Codelabs documentation,README|
| Nidhi Nitin Kulkarani   |      36    | Airflow Integration for pipelines - Web scraping, S3 and Snowflake Upload, Airflow trigger via Streamlit, Dockerization of Airflow, Streamlit and FastAPI, Deployment on Cloud |
| Deepakraja Rajendran   |     32     | Streamlit Web-App for S3 and Snowflake Integration, 2 FastAPI services for S3 integration and snowflake, Docker, S3 bucket handling, README, Codelabs documentation|
