from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    # def ready(self):
    #     import blog.signals  # Assuming your signal is in a file named signals.py within the jobs app