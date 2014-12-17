from time import time
from random import randrange

HITS_DEFAULT = 0

class Algorithm(object):
    LRU = 1
    MRU = 2
    RR  = 3
    LFU = 4


class EasyCache(object):

    def __init__(self, capacity=100, timeout=180, algorithm=Algorithm.LRU):
        self.capacity = capacity
        self.timeout = timeout
        self.algorithm = algorithm
        self._cache = {}


    def remove(self, key):
        try:
            self._cache = dict(self._cache)
            del self._cache[key]
            return True
        except:
            return False


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
