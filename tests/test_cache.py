from time import sleep
from easy_cache.cache import EasyCache
from easy_cache.cache import Algorithm
from unittest import TestCase

class TestCache(TestCase):

    def test_cache_get_insertion(self):
        c = EasyCache(1)
        c.set('a_key', 'a_value')
        assert c.get('a_key') == 'a_value'

    def test_cache_size_limit(self):
        c = EasyCache(3)
        c.set('a_key', 'a_value')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        assert c.get('a_key') == 'a_value'
        assert c.get('b_key') == 'b_value'
        assert c.get('c_key') == 'c_value'

    def test_cache_get_default_insertion(self):
        c = EasyCache(1)
        c.get('a_key', default='a_value')
        assert c.get('a_key') == 'a_value'

    def test_cache_timeout(self):
        c = EasyCache(1, timeout=2)
        c.set('a_key', 'a_value')
        assert c.get('a_key') == 'a_value'
        sleep(2)
        assert c.get('a_key') == None

    def test_cache_LRU_polici(self):
        c = EasyCache(3, algorithm = Algorithm.LRU)
        c.set('a_key', 'a_value')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        sleep(0.01)
        c.get('b_key')
        c.get('a_key')
        c.set('d_key', 'd_value')
        assert c.get('c_key') == None
        assert c.get('d_key') == 'd_value'
        assert c.get('a_key') == 'a_value'
        assert c.get('b_key') == 'b_value'

    def test_cache_MRU_polici(self):
        c = EasyCache(3, algorithm = Algorithm.MRU)
        c.set('a_key', 'a_value')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        sleep(0.01)
        c.get('b_key')
        c.get('a_key')
        assert c.get('d_key') == None
        assert c.get('c_key') == 'c_value'
        assert c.get('a_key') == 'a_value'
        assert c.get('b_key') == 'b_value'

    def test_cache_LFU_polici(self):
        c = EasyCache(3, algorithm = Algorithm.LFU)
        c.set('a_key', 'a_value')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        sleep(0.01)
        c.get('b_key')
        c.get('a_key')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        c.set('a_key', 'a_value')
        c.set('d_key', 'd_value')
        assert c.get('c_key') == None
        assert c.get('d_key') == 'd_value'
        assert c.get('a_key') == 'a_value'
        assert c.get('b_key') == 'b_value'

    def test_clear_cache(self):
        c = EasyCache(3, algorithm = Algorithm.LFU)
        c.set('a_key', 'a_value')
        c.set('b_key', 'b_value')
        c.set('c_key', 'c_value')
        c.clear()
        assert c.get('a_key') == None
        assert c.get('b_key') == None
        assert c.get('c_key') == None






