from django.apps import AppConfig

class ReceiversApi(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.receivers.infra.django_ninja_app'
    label = 'receivers'
    verbose_name = 'Receivers'