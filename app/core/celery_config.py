import os
from functools import lru_cache
from kombu import Queue


def route_task(name, args, kwargs, options, task=None, **kw):
	"""
	Support routing by name prefix: 'queue_name:task_name'
	e.g. name='qrcode:create_task' -> queue 'qrcode'
	Fallback to default 'celery' queue.
	"""
	if ":" in name:
		queue, _ = name.split(":", 1)
		return {"queue": queue}
	return {"queue": "celery"}


class BaseConfig:
	# Broker (RabbitMQ by default)
	CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
	# Result backend (Redis by default)
	CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

	# Queues: default + feature queues
	CELERY_TASK_QUEUES = (
		Queue("celery"),
		Queue("qrcode"),
		Queue("barcode"),
	)

	CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
	pass


@lru_cache()
def get_settings():
	config_cls_dict = {
		"development": DevelopmentConfig,
	}
	config_name = os.environ.get("CELERY_CONFIG", "development")
	return config_cls_dict[config_name]()


settings = get_settings()

