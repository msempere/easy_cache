from time import time


class Algorith(object):
    LRU = 1
    # TODO MRU = 2
    # TODO RR  = 3
    # TODO LFU = 4


class EasyCache(object):

    def __init__(self, capacity=100, timeout=180, algorith=Algorith.LRU):
        self.capacity = capacity
        self.timeout = 180
        self.algorith = algorith
        self._cache = {}

    def remove(self, key):
        if key in self._cache:
            self._cache = dict(self._cache)
            del self._cache[key]

    def _purgue(self):
        if len(self._cache) > self.capacity:
            num_items_to_remove = len(self._cache) - self.capacity

            if self.algorith == Algorith.LRU:
                sorted_cache = sorted(self._cache.items(), key=lambda x: x[1][3])

                for item in range(0 , num_items_to_remove - 1):
                    self.remove(sorted_cache.items()[0][0])

    def get(self, key):
        try:
            eviction, value, hits, used = self._cache[key]

            if eviction < time():
                self.remove(key)
                return None
            else:
                return value
        except KeyError:
            return None

    def set(self, key, value, timeout=None):
        timeout = self.timeout if not timeout else timeout
        try:
            if key in self._cache:
                _eviction, _value, _hits, _used = self._cache[key]
                self._cache[key] = (_eviction, value, _hits + 1, time())
            else:
                self._cache[key] = (time() + timeout, value, 0, time() + timeout)
                self._purgue()
            return True
        except:
            return False
