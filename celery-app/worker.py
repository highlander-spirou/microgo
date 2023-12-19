from celery import Celery

BROKER_URL = 'amqp://accessuser:accesspwd@localhost:5672/first-vhost'
BACKEND_URL = 'mongodb://root:secret@localhost:27017?authSource=admin'


task_consumer = Celery('task_consumer', broker=BROKER_URL, backend=BACKEND_URL)


@task_consumer.task(name='log_arg')
def crawl_data(arg):
    print(arg)
    return arg


if __name__ == '__main__':
    args = ['worker', '-Q', 'celery_images', '--loglevel=INFO', '--concurrency=2']
    task_consumer.worker_main(argv=args)