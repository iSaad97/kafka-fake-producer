from confluent_kafka import Producer as p
from confluent_kafka.admin import AdminClient,NewTopic


import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('kafka_logs')
BROKER_URL = 'PLAINTEXT://localhost:9092'

class Producer:
    existing_topics = set([])
    def __init__(self,
                 topic_name,
                 num_partitions=3,
                 num_replicas=1):

        self.topic_name = topic_name
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas
        self.broker_properties = {
            'bootstrap.servers':BROKER_URL
        }



        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = p(self.broker_properties)

    def create_topic(self):
        client = AdminClient({'bootstrap.servers':BROKER_URL})
        if self.topic_exists(client,self.topic_name) is False:
            futures = client.create_topics(

                [
                    NewTopic(
                        topic=self.topic_name,
                        num_partitions=self.num_partitions,
                        replication_factor=self.num_replicas
                    )
                ]
            )

            for topic,future in futures.items():
                try:
                    future.result()
                    logger.info('topic created')
                except Exception as e:
                    logger.warn(f'{self.topic_name} failed to be created')
        else:
            logger.info(f'{self.topic_name} topic already exist')



    def topic_exists(self,client,topic_name):
        topic_metadata = client.list_topics(timeout=5)
        return topic_name in set(t.topic for t in iter(topic_metadata.topics.values()))

    def close(self):
        self.producer.flush()
        logger.info('producer closed')

