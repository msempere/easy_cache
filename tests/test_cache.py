from time import sleep, time
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

    def test_cache_memoize(self):
        c = EasyCache()

        @c.cached()
        def foo():
            return time()

        result_1 = foo()
        sleep(0.1)
        result_2 = foo()
        assert result_1 == result_2

    def test_cache_class_type(self):
        c = EasyCache(timeout=0.5)

        class A(object):
            value = "a_value"

        c.set('a_key', A)
        assert c.get('a_key').value == "a_value"

    def test_cache_class_different_type(self):
        c = EasyCache(timeout=0.5)

        class A(object):
            value = "a_value"

        c.set('a_key', A)
        c.set('b_key', 1)
        assert c.get('a_key').value == "a_value"
        assert c.get('b_key') == 1

    def test_cache_memoize_with_timeout(self):
        c = EasyCache(timeout=0.5)

        @c.cached()
        def foo():
            return time()

        result_1 = foo()
        sleep(0.1)
        result_2 = foo()
        assert result_1 == result_2
        sleep(0.5)
        result_3 = foo()
        assert result_3 != result_1

    def test_cache_memoize_with_parameters(self):
        c = EasyCache()

        @c.cached()
        def foo(a=1, b=2):
            return time()

        assert foo(1,2) == foo(1) == foo() == foo(b=2) == foo(a=1) == foo(a=1, b=2)
        assert foo(1,2) != foo(2,1)

    def test_cache_memoize_with_different_classes(self):
        c = EasyCache()
        class A(object):
            @c.cached()
            def foo(self):
                return 'A'

        class B(object):
            @c.cached()
            def foo(self):
                return 'B'
        a = A()
        b = B()
        assert a.foo() != b.foo() and a.foo() != b.foo()
        assert a.foo() == 'A' and b.foo() == 'B'

    def test_cache_memoize_with_same_class_different_instance(self):
        c = EasyCache()
        class A(object):
            def __init__(self):
                self.i = 0

            @c.cached()
            def get(self):
                return self.i

        a = A()
        b = A()
        a.i = 2
        b.i = 1
        assert a.get() == 2 and b.get() == 1
        a.i = 1
        b.i = 2
        assert a.get() == 2 and b.get() == 1

    def test_cache_memoize_with_same_class_different_instance_and_default_parameters(self):
        c = EasyCache()
        class A(object):
            def __init__(self):
                self.i = 0

            @c.cached()
            def get(self, a=1, b=5):
                return a + self.i

        a = A()
        b = A()
        a.i = 1
        b.i = 2

        assert a.get() == 2 and b.get() == 3
        assert a.get(1, 5) == 2 and a.get(1) == 2 and a.get(b=5, a=1) == 2 and b.get(1) == 3 and b.get(a=1, b=5) == 3

