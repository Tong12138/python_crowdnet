from django.apps import AppConfig
# from django.utils.module_loading import autodiscover_modules

class BaseConfig(AppConfig):
    name = 'base'

    # def ready(self):
    #     autodiscover_modules("start")
