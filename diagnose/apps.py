from django.apps import AppConfig


class DiagnoseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diagnose'
    
    def ready(self) -> None:
        import diagnose.signals
