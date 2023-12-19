from celery import Celery
from kombu import Exchange, Queue, Connection

BROKER_URL = 'amqp://accessuser:accesspwd@localhost:5672/first-vhost'
BACKEND_URL = 'mongodb://accessuser:accesspwd@localhost:27017?authSource=admin'

task_producer = Celery('task_producer', broker=BROKER_URL, backend=BACKEND_URL)
task_producer.conf.task_routes = {
    "log_arg": {"exchange": "celery_images", "routing_key": "celery_images"},
}


if __name__ == '__main__':
    print('dispatching task')
    task = task_producer.send_task('log_arg', kwargs={"arg": 'hello world'}, route_name='log_arg')