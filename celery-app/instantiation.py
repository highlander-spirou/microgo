"""
Singleton global modules: FileAccess, Auth
"""
from config import config
from file_access import FileAccess
from auth import UserAuthentication
from message_queue import TaskProducer


authenticator = UserAuthentication(config)
file_access = FileAccess(config)
task_producer = TaskProducer(config)