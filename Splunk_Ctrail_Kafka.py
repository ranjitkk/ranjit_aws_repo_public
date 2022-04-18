import json
import time 
from time import time
from confluent_kafka import Producer
import io
#import re
import gzip
import boto3
import os
from botocore.exceptions import ClientError

KAFKA_BROKER = 'b-3-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196,b-1-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196,b-2-public.splunktestcluster.w0qk57.c2.kafka.us-east-1.amazonaws.com:9196'
KAFKA_TOPIC = 'TestTopic'

producer = Producer({
    'bootstrap.servers':KAFKA_BROKER,
    'socket.timeout.ms':100,
    'security.protocol':'sasl_ssl',
    'sasl.mechanism':'SCRAM-SHA-512',
    'sasl.username':'connect_user',
    'sasl.password':'Pa$$1234'
    #'ssl.ca.location':'/etc/ssl/certs/'
    })

def get_records(session, bucket, key):
    """
    Loads a CloudTrail log file, decompresses it, and extracts its records.
    :param session: Boto3 session
    :param bucket: Bucket where log file is located
    :param key: Key to the log file object in the bucket
    :return: list of CloudTrail records
    """
    s3 = session.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)

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
    print("Sending message")
    try:
        msg_json_str = str({"data": json.dumps(msg)})
        producer.produce(
            KAFKA_TOPIC,
            msg_json_str,
            callback=lambda err, original_msg=msg_json_str: delivery_report(err, original_msg
                                                                            ),
        )
        producer.flush()
    except Exception as ex:
        print("Error : ", ex)

if __name__ == "__main__":
    session = boto3.session.Session()
    s3 = session.client('s3')
    s3_bucket = 'cloudtrail-awslogs-647604195155-jg8ehymb-isengard-do-not-delete'
    s3_key = 'AWSLogs/647604195155/CloudTrail/us-east-1/2019/08/23/647604195155_CloudTrail_us-east-1_20190823T1905Z_uUeu464Gv2PHUJ55.json.gz'
    records = get_records(session,s3_bucket,s3_key)
    print("Records to be processed: ",len(records))
    start_time = int(time() * 1000)
    for item in records:
        data = item
        send_msg_async(data)
    end_time = int(time() * 1000)
    time_taken = (end_time - start_time) / 1000
    print("Time taken to complete = %s seconds" % (time_taken))