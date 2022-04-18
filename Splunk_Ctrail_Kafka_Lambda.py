import json
import time 
from time import time
from confluent_kafka import Producer
import io
import gzip
import boto3
import os
from botocore.exceptions import ClientError

KAFKA_BROKER = os.environ['MSK_BROKER']
KAFKA_TOPIC  = os.environ['MSK_TOPIC']
SECRET_ID = os.environ['SECRET_ID']
# KAFKA_BROKER = 'b-3-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196,b-1-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196,b-2-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196'
# KAFKA_TOPIC = 'TestTopic'

def get_records(session, bucket, key):
    """
    Loads a CloudTrail log file, decompresses it, and extracts its records.
    :param session: Boto3 session
    :param bucket: Bucket where log file is located
    :param key: Key to the log file object in the bucket
    :return: list of CloudTrail records
    """
    s3 = session.client('s3')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except ClientError as e:
        print("S3 Get Object Error:", e.response)
        raise
    with io.BytesIO(response['Body'].read()) as obj:
        with gzip.GzipFile(fileobj=obj) as logfile:
            try:
                records = json.load(logfile)['Records']        
            except KeyError:
                return False
            else:
                return records



def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(
            msg.topic(), msg.partition()))

def send_msg_async(msg):
    # print("Sending message")
    try:
        # msg_json_str = str({"sourcetype": "aws:cloudtrail", "event": msg})
        msg_json_str = str(json.dumps(msg))
        producer.produce(
            KAFKA_TOPIC,
            msg_json_str,
            callback=lambda err, original_msg=msg_json_str: delivery_report(err, original_msg),
        )
        # producer.flush()
    except Exception as ex:
        print("Error : ", ex)

def lambda_handler(event, context):
    session = boto3.session.Session()
    secret = session.client('secretsmanager')
    try:
        secret_response = secret.get_secret_value(
    SecretId=SECRET_ID)
    except ClientError as e:
        print("Secret Manager error:", e.response)
        raise
    else:
        secret_key = json.loads(secret_response['SecretString'])
    producer = Producer({
    'bootstrap.servers':KAFKA_BROKER,
    'socket.timeout.ms':100,
    'security.protocol':'sasl_ssl',
    'sasl.mechanism':'SCRAM-SHA-512',
    'sasl.username':secret_key['username'],
    'sasl.password':secret_key['password']
    #'ssl.ca.location':'/etc/ssl/certs/'
    })
    for record in event['Records']:
        msg_body = json.loads(record['body'])
        s3_bucket = msg_body['Records'][0]['s3']['bucket']['name']
        s3_key = msg_body['Records'][0]['s3']['object']['key']
        print("S3 Object Key:",s3_key)
        records = get_records(session,s3_bucket,s3_key)
        print("Records to be processed: ",len(records))
        start_time = int(time() * 1000)
        for item in records:
            send_msg_async(item)
        end_time = int(time() * 1000)
        time_taken = (end_time - start_time) / 1000
        print("Time taken to process kafka = %s seconds" % (time_taken))