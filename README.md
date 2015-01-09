![Logo](http://i.imgur.com/HDXDpCo.png)

# easy_cache [![Build Status](https://travis-ci.org/msempere/easy_cache.svg?branch=master)] (http://travis-ci.org/msempere/easy_cache)

## Versions:
* master [![Build Status](https://travis-ci.org/msempere/easy_cache.svg?branch=master)](https://travis-ci.org/msempere/easy_cache.svg?branch=master) 


Easy in-memory key-value cache for single-threaded environments

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
from easy_cache.cache import EasyCache, Algorithm

c = EasyCache(capacity = 10, algorith = Algorithm.LRU)
c.set('a_key', 'a_value', timeout = 3*60)
c.get('a_key') # got 'a_value'
c.get('a_key') # got 'a_value'
c.get('a_key') # got None after 3*60 seconds

c.get('another_key', default='another_value') # if key is not available sets default value
c.get('another_key') # got 'another_value'
```

## Memoization example

```python
from easy_cache.cache import EasyCache

cache = EasyCache(timeout = 10) # memoize for 10 seconds

cache.cached()
def foo()
  return time()
  
foo() got # 1419007127.181711
foo() got # 1419007127.181711
sleep(10)
foo() got # 1419007137.192731
```


