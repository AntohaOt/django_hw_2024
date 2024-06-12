"""
This module contains the configuration for the 'main' Django application.

The `MainConfig` class extends `AppConfig` and sets the default auto field type and the application name.
"""

from django.apps import AppConfig


class MainConfig(AppConfig):
    """Configuration for the 'main' Django application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
