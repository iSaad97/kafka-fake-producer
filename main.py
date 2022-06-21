import time
import os
import random

from Producer import Producer
import json

log_type_list = ['WARNING','INFO','CRITICAL','DEBUG']


def get_logs(log):
    log_content = log.split('|')
    log_date = log_content[0].strip()
    log_type = log_content[1].strip()
    log_name = log_content[2].strip()
    log_thread = log_content[3].strip()
    log_issued_path = log_content[4].strip()
    log_message = log_content[-1].strip()

    return log_date, log_type, log_name, log_thread, log_issued_path, log_message

if __name__ == '__main__':
    kafka_producer = Producer(topic_name='fake_producer')
    while(True):

        log = fr'[{time.asctime()}] | [{random.choice(log_type_list)}] | [MSSQL LOGGER] | [Thread-2] | [C:\Users\n736109.NICINT\Desktop\DE-TOOLS\BackEnd\flasker\api\database_connectors\connect_to_source_db_mssql.py] | : | [Successfully connected to saad_kt database.]'
        log_date, log_type, log_name, log_thread, log_issued_path, log_message = get_logs(log)

        value = json.dumps({"date": log_date,"type": log_type,"name": log_name,"thread": log_thread,"issued path": log_issued_path, "message": log_message,"user": os.getlogin()})
        kafka_producer.producer.poll(0)
        kafka_producer.producer.produce(topic='fake_producer',
                                        key='mssql_log',
                                        value=value)
        kafka_producer.producer.flush()

        time.sleep(0.5)
