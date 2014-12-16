easy_cache
==========

Easy memory cache for single-threaded environments

Usage example:

```python
from easy_cache.cache import EasyCache

c = EasyCache(capacity=1, algorith=Algorith.LRU)
c.set('a_key', 'a_value', timeout=10)
c.get('a_key') # got 'a_value'
c.get('a_key') # got 'a_value'
c.get('a_key') # got nothing
```
