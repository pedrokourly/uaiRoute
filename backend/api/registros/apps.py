from django.apps import AppConfig

class RegistrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.registros'  # ✅ isso precisa estar certo
