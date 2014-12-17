"""
    easy_cache
    ----------
    Easy key-value cache for single-threaded environments.

    Usage example:
    =============

    >>> from easy_cache.cache import EasyCache, Algorithm
    >>> c = EasyCache(capacity = 10, algorith = Algorithm.LRU)
    >>> c.set('a_key', 'a_value', timeout = 3*60)
    >>> c.get('a_key')
    'a_value'
    >>> c.get('a_key')
    'a_value'
    >>> c.get('a_key')
    >>>
"""

from time import time
from random import randrange

HITS_DEFAULT = 0

class Algorithm(object):
    LRU = 1
    MRU = 2
    RR  = 3
    LFU = 4


class EasyCache(object):
    """Easy key-value cache for single-threaded environments.
    :param capacity: maximum number if items to store before start deleting following the replacement policy
    :param timeout: default timeout to apply if timeout is not set when storing keys
    :param algorithm: replacement policy to use when the capacity is reached
    """

    def __init__(self, capacity=100, timeout=180, algorithm=Algorithm.LRU):
        self.capacity = capacity
        self.timeout = timeout
        self.algorithm = algorithm
        self._cache = {}


    def remove(self, key):
        return self._cache.pop(key, None) is not None

    def clear(self):
        self._cache.clear()

    def _purge(self):
        if len(self._cache) >= self.capacity:
            num_items_to_remove = 1 + ( len(self._cache) - self.capacity )

            if self.algorithm == Algorithm.RR:
                for item in range(0 , num_items_to_remove - 1):
                    self.remove(self._cache[0][randrange(0,len(self.cache) - 1)])
            else:
                sorted_cache = []
                if self.algorithm == Algorithm.LRU:
                    sorted_cache = sorted(self._cache.items(), key=lambda x: x[1][3])

                elif self.algorithm == Algorithm.MRU:
                    sorted_cache = sorted(self._cache.items(), key=lambda x: x[1][3], reverse=True)

                elif self.algorithm == Algorithm.LFU:
                    sorted_cache = sorted(self._cache.items(), key=lambda x: x[1][2])

                for item in range(0 , num_items_to_remove):
                    self.remove(sorted_cache[0][0])


    def get(self, key, default=None):
        try:
            eviction, value, hits, used = self._cache[key]

            if eviction < time():
                self.remove(key)
                return None
            else:
                _eviction, _value, _hits, _used = self._cache[key]
                self._cache[key] = (_eviction, _value, _hits + 1, time())
                return _value
        except KeyError:
            if default:
                self.set(key, default)
                return default
            return None


    def set(self, key, value, timeout=None):
        timeout = self.timeout if not timeout else timeout
        try:
            if key in self._cache:
                _eviction, _value, _hits, _used = self._cache[key]
                self._cache[key] = (_eviction, value, _hits + 1, time())
            else:
                self._purge()
                self._cache[key] = (time() + timeout, value, HITS_DEFAULT, time())
            return True
        except:
            return False
