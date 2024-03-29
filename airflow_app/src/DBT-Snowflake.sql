create warehouse Assignment4;
create database raw_test;
create database raw_prod;
create database clean_test;
create database clean_prod;
create schema raw_test.cfa;
create schema raw_test.pdf;
create schema raw_prod.cfa;
create schema raw_prod.pdf;


create table raw_test.cfa.ctable
( Name_of_the_topic varchar,
  Year integer,
  Level integer,
  Introduction_Summary varchar,
  Learning_Outcomes varchar,
  Link_to_the_Summary_Page varchar,
  Link_to_the_PDF_File varchar
); 

create table raw_prod.cfa.ctable
( Name_of_the_topic varchar,
  Year integer,
  Level integer,
  Introduction_Summary varchar,
  Learning_Outcomes varchar,
  Link_to_the_Summary_Page varchar,
  Link_to_the_PDF_File varchar
); 

create table raw_test.pdf.ptable
( File_Name varchar,
  Heading_Topic varchar,
  Sub_Headings varchar,
  Count integer
);   


COPY INTO raw_test.cfa.ctable
	FROM 's3://airflow-cfa/CFA.csv'
	CREDENTIALS=(AWS_KEY_ID='' AWS_SECRET_KEY='')
	FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF=('<NULL>', 'NULL', ''))
	ON_ERROR = 'CONTINUE';

COPY INTO raw_test.pdf.ptable
	FROM 's3://airflow-cfa/final_output.csv'
	CREDENTIALS=(AWS_KEY_ID='' AWS_SECRET_KEY='')
	FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF=('<NULL>', 'NULL', ''))
	ON_ERROR = 'CONTINUE'; 


create table raw_prod.pdf.ptable
( File_Name varchar,
  Headings varchar,
  Topics varchar,
  Topics_Count integer
); 

COPY INTO raw_prod.pdf.ptable
	FROM 's3://airflow-cfa/final_output.csv'
	CREDENTIALS=(AWS_KEY_ID='' AWS_SECRET_KEY='')
	FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF=('<NULL>', 'NULL', ''))
	ON_ERROR = 'CONTINUE'; 

COPY INTO raw_prod.cfa.ctable
	FROM 's3://airflow-cfa/CFA.csv'
	CREDENTIALS=(AWS_KEY_ID='' AWS_SECRET_KEY='')
	FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1 NULL_IF=('<NULL>', 'NULL', ''))
	ON_ERROR = 'CONTINUE';
