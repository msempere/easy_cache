easy_cache
==========

Easy memory cache for single-threaded environments

## Install
```
python setup.py install
```

## Supported replacement policies
- LRU (Least Recently Used)
- MRU (Most Recently Used)
- RR (Random Replacement)
- LFU (Least-Frequently Used)

## Usage example

```python
from easy_cache.cache import EasyCache

c = EasyCache(capacity = 10, algorith = Algorith.LRU)
c.set('a_key', 'a_value', timeout = 3*60)
c.get('a_key') # got 'a_value'
c.get('a_key') # got 'a_value'
c.get('a_key') # got nothing

c.get('another_key', default='another_value') # if key is not available sets default value
```
