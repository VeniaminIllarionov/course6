from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_qs_from_cache(qs, key):
    if not CACHE_ENABLED:
        return qs
    objects = cache.get(key)
    if objects is not None:
        return objects
    objects = qs
    cache.set(key, qs)
    return objects

