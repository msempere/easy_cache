from easy_cache.cache import EasyCache
from unittest import TestCase

class TestCache(TestCase):

    def test_cache_get_insertion(self):
        c = EasyCache(1)
        c.set('a_key', 'a_value')
        assert c.get('a_key') == 'a_value'

    def test_cache_get_default_insertion(self):
        c = EasyCache(1)
        c.get('a_key', default='a_value')
        assert c.get('a_key') == 'a_value'





