from django.apps import AppConfig





class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'  # 👈 这里要改成 apps.users

