from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import PyPDF2
import pandas as pd
import re

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 28),
}

dag = DAG(
    'process_pdf_dag',
    default_args=default_args,
    description='A DAG to process text from a PDF file',
    schedule_interval=None,
)

def read_pdf_text(**kwargs):
    pdf_path = kwargs['pdf_path']
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
    kwargs['ti'].xcom_push(key='pdf_text', value=text)

def process_extracted_text(**kwargs):
    ti = kwargs['ti']
    text_data = ti.xcom_pull(key='pdf_text', task_ids='extract_text_from_pdf')

    def extract_titles_from_text(text):
        pattern = re.compile(r'(?P<title>[A-Z][\w\s]+)\nLEARNING OUTCOMES', re.MULTILINE)
        titles = []
        for match in pattern.finditer(text):
            title = match.group("title").strip()
            lines = title.split("\n")
            last_line_words = lines[-1].split()
            if len(last_line_words) == 1 and len(lines) > 1:
                pre_last_line_words = lines[-2].split()
                if len(pre_last_line_words) >= 2 and all(word[0].isupper() for word in pre_last_line_words):
                    title = f"{lines[-2]} {last_line_words[0]}"
            titles.append(title)
        return titles

    titles_before_outcomes = extract_titles_from_text(text_data)
    lines = text_data.split("\n")
    data = []
    current_topic = ""
    current_heading = ""
    outcome = ""

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line == "LEARNING OUTCOMES":
            continue
        if line[0].isupper() and not line.startswith("□") and not "The candidate should be able to" in line:
            if current_topic and current_heading and outcome:
                data.append([current_topic, current_heading, outcome.strip("□ ").replace("\n", " ")])
                outcome = ""
            current_topic = line if line in titles_before_outcomes else current_topic
            current_heading = "" if line in titles_before_outcomes else line
        elif line.startswith("□") or "The candidate should be able to" in line:
            if outcome:
                data.append([current_topic, current_heading, outcome.strip("□ ").replace("\n", " ")])
                outcome = ""
            outcome = line
        if i == len(lines) - 1 and outcome:
            data.append([current_topic, current_heading, outcome.strip("□ ").replace("\n", " ")])

    df = pd.DataFrame(data, columns=["Topic", "Heading", "Learning Outcomes"])
    
    def clean_learning_outcome(val):
        val = val.replace('\t', ' ')
        cleaned_val = re.sub(r'[^\w\s.-]', '', val)
        if not cleaned_val.endswith('.'):
            cleaned_val += '.'
        return cleaned_val.capitalize()

    def clean_topics(val):
        return re.sub(r'\d+', '', val)

    df['Learning Outcomes'] = df['Learning Outcomes'].apply(clean_learning_outcome)
    df['Topic'] = df['Topic'].apply(clean_topics)

    # Example: Save the DataFrame to a CSV file
    df.to_csv("/opt/airflow/CSV/processed_data.csv", index=False)

with dag:
    extract_text = PythonOperator(
        task_id='extract_text_from_pdf',
        python_callable=read_pdf_text,
        op_kwargs={'pdf_path': '/opt/airflow/CSV/example.pdf'},
    )

    process_text = PythonOperator(
        task_id='process_extracted_text',
        python_callable=process_extracted_text,
    )

    extract_text >> process_text
