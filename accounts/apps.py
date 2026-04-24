# --------------------------------------------------
# Django application configuration for the accounts app
# This class is used to configure application-level settings
# and run startup code when the Django app is ready.
# --------------------------------------------------

from django.apps import AppConfig


class AccountsConfig(AppConfig):

    # --------------------------------------------------
    # Specifies the default type for automatically created
    # primary key fields for models in this app.
    #
    # BigAutoField is recommended for modern Django projects
    # because it supports a larger range of IDs.
    # --------------------------------------------------
    default_auto_field = 'django.db.models.BigAutoField'

    # --------------------------------------------------
    # The name of the application.
    # This must match the folder name of the app.
    # --------------------------------------------------
    name = 'accounts'

    # --------------------------------------------------
    # The ready() method is executed when Django starts
    # and the application registry is fully loaded.
    #
    # Here we import the signals module to ensure that
    # all signal handlers (e.g., post_delete) are registered.
    #
    # Without this import, Django might not load the signals
    # and they would never be triggered.
    # --------------------------------------------------
    def ready(self):
        import accounts.signals
