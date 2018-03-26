"""Module for all rizzanet views"""
from .main import register_routes
from .extentions import bind_jinja2_functions
__all__ = ['.main','.extentions']
