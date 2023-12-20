from celery import Celery
from dataclasses import dataclass

@dataclass
class TaskProducer:
    config: dict

    def __post_init__(self):
        username = self.config.get('ACCESS_USR')
        pwd = self.config.get('ACCESS_PWD')

        broker_host = self.config.get('BROKER_HOST')
        broker_port = self.config.get('BROKER_PORT')
        broker_vhost = self.config.get('BROKER_VHOST')

        backend_host = self.config.get('MONGO_HOST')
        backend_port = self.config.get('MONGO_PORT')

        BROKER_URL = f'amqp://{username}:{pwd}@{broker_host}:{broker_port}/{broker_vhost}'
        BACKEND_URL = f'mongodb://{username}:{pwd}@{backend_host}:{backend_port}?authSource=admin'

        self.task_producer = Celery('task_producer', broker=BROKER_URL, backend=BACKEND_URL)

        self.task_producer.conf.task_routes = {
            "process_img": {"exchange": "celery_images", "routing_key": "celery_images"},
        }

    def dispatch_img_task(self, fs_id):
        self.task_producer.send_task('img_process', kwargs={"fs_id": fs_id}, route_name='process_img')

# task_producer = Celery('task_producer', broker=BROKER_URL, backend=BACKEND_URL)


# if __name__ == '__main__':
#     print('dispatching task')
#     task = task_producer.send_task('log_arg', kwargs={"arg": 'hello world'}, route_name='log_arg')