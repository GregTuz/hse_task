import base64
import sys
import datetime
import logging
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
from confluent_kafka import Producer
import fastavro
from io import BytesIO

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('hse_logger')
logger.setLevel(logging.INFO)

avro_schema = {
	"type": "record",
	"name": "UserRecord",
	"fields": [
		{"name": "user_id", "type": "string"},
		{"name": "name", "type": "string"},
		{"name": "email", "type": "string"},
		{"name": "location", "type": "string"},
		{"name": "phone", "type": "string"},
		{"name": "cell", "type": "string"},
		{"name": "dob", "type": "string"},
		{"name": "nat", "type": "string"}
	]
}

def fetch_data(**kwargs):
	r = requests.get('https://randomuser.me/api/?results=5')
	data = r.json().get('results')
	kwargs['ti'].xcom_push(key='user_data', value=data)
	logger.info(f"Fetched {len(data)} users from API.")


def save_to_mongo(**kwargs):
	client = MongoClient("mongodb://mongo_user:mongo_password@mongo:27017/")
	db = client['hse_task_mongo']
	collection = db['users']
	ti = kwargs['ti']
	data = ti.xcom_pull(task_ids='fetch_data', key='user_data')
	if data:
		collection.insert_many(data)
		logger.info("Data successfully written to users in hse_task_mongo")


def process_location_data(**kwargs):
	ti = kwargs['ti']
	data = ti.xcom_pull(task_ids='fetch_data', key='user_data')

	location_data = []
	for user in data:
		location = user.get('location')
		location_str = f"{location.get('city')}, {location.get('state')}, {location.get('country')}"
		location_data.append(location_str)

	kwargs['ti'].xcom_push(key='location_data', value=location_data)
	logger.info(f"Processed location data for {len(location_data)} users.")


def process_user_data(**kwargs):
	ti = kwargs['ti']
	data = ti.xcom_pull(task_ids='fetch_data', key='user_data')
	location_data = ti.xcom_pull(task_ids='process_location_data', key='location_data')

	user_data = []
	for idx, user in enumerate(data):
		location_str = location_data[idx]
		name = f"{user['name']['title']} {user['name']['first']} {user['name']['last']}"

		user_record = {
			"user_id": user['login']['uuid'],
			"name": name,
			"email": user['email'],
			"location": location_str,
			"phone": user['phone'],
			"cell": user['cell'],
			"dob": user['dob']['date'],
			"nat": user['nat']
		}
		user_data.append(user_record)

	avro_data = []
	for record in user_data:
		bytes_writer = BytesIO()
		fastavro.writer(bytes_writer, avro_schema, [record])
		avro_bytes = bytes_writer.getvalue()

		avro_data.append(base64.b64encode(avro_bytes).decode('utf-8'))

	kwargs['ti'].xcom_push(key='avro_data', value=avro_data)
	logger.info(f"Processed {len(user_data)} users for Avro.")


def send_to_kafka(**kwargs):
	producer = Producer({'bootstrap.servers': 'broker:9092'})

	ti = kwargs['ti']
	avro_data = ti.xcom_pull(task_ids='process_user_data', key='avro_data')

	if avro_data:
		for record in avro_data:
			producer.produce('user_data_avro_topic', value=record)
		producer.flush()
		logger.info(f"Sent {len(avro_data)} Avro records to Kafka topic 'user_data_avro_topic'.")


with DAG(
		'Process_api',
		default_args={
			'owner': 'admin',
			'depends_on_past': False,
			'start_date': datetime.datetime(2025, 4, 2),
			'retries': 1,
			'retry_delay': datetime.timedelta(minutes=5),
		},
		schedule=datetime.timedelta(minutes=15),
		catchup=False,
) as dag:

	fetch_data_task = PythonOperator(
		task_id='fetch_data',
		python_callable=fetch_data,
		provide_context=True
	)

	save_to_mongo_task = PythonOperator(
		task_id='save_to_mongo',
		python_callable=save_to_mongo,
		provide_context=True
	)

	process_location_data_task = PythonOperator(
		task_id='process_location_data',
		python_callable=process_location_data,
		provide_context=True
	)

	process_user_data_task = PythonOperator(
		task_id='process_user_data',
		python_callable=process_user_data,
		provide_context=True
	)

	send_to_kafka_task = PythonOperator(
		task_id='send_to_kafka',
		python_callable=send_to_kafka,
		provide_context=True
	)

	fetch_data_task >> [save_to_mongo_task, process_location_data_task, process_user_data_task]
	process_location_data_task >> send_to_kafka_task
	process_user_data_task >> send_to_kafka_task
