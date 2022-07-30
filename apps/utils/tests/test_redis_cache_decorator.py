import json
from unittest.mock import MagicMock, patch

from django.conf import settings
import pytest
from redis.exceptions import ConnectionError

from apps.utils.helpers import redis_cache


class TestRedisCache:
    EXPECTED_RESULT = {"test_key": "test_value"}

    func = MagicMock(return_value=EXPECTED_RESULT)
    func.__qualname__ = "MagicMock"

    RedisGetMock = MagicMock()
    RedisGetMock().__enter__().get.return_value = json.dumps(EXPECTED_RESULT)

    RedisSetMock = MagicMock()
    RedisSetMock().__enter__().get.return_value = None

    @pytest.fixture(autouse=True)
    def tear_down(self):
        yield
        self.func.reset_mock()
        self.RedisGetMock.reset_mock()
        self.RedisSetMock.reset_mock()

    @patch("apps.utils.helpers.StrictRedis.from_url", side_effect=RedisGetMock)
    def test_redis_cache_loads_cached_value_from_redis(self, *args):
        decorated_func = redis_cache(redis_url="redis://test")(self.func)
        decorated_func()
        result = decorated_func()

        assert result, self.EXPECTED_RESULT
        assert self.func.call_count == 0
        assert self.RedisGetMock().__enter__().get.call_count == 2

    def test_redis_cache_calls_function_when_redis_url_is_empty(self):
        func = MagicMock(return_value={"test_key": "test_value"})
        decorated_func = redis_cache(redis_url="")(func)
        decorated_func()
        result = decorated_func()

        assert func.call_count == 2
        assert result == self.EXPECTED_RESULT

    @patch("apps.utils.helpers.StrictRedis.from_url", side_effect=RedisSetMock)
    def test_redis_cache_stores_value_with_default_ttl_to_redis(self, *args):
        decorated_func = redis_cache(redis_url="redis://test")(self.func)
        result = decorated_func()

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1
        assert self.RedisSetMock().__enter__().setex.call_count == 1
        self.RedisSetMock().__enter__().setex.assert_called_once_with(
            '{"__module__": "unittest.mock", "__qualname__": "MagicMock", "args": [], "kwargs": {}}',
            settings.REDIS_CACHE_DEFAULT_TTL,
            '{"test_key": "test_value"}',
        )

    @patch("apps.utils.helpers.StrictRedis.from_url", side_effect=RedisSetMock)
    def test_redis_cache_stores_value_with_given_ttl_to_redis(self, *args):
        ttl = 60
        decorated_func = redis_cache(ttl=ttl, redis_url="redis://test")(self.func)
        result = decorated_func()

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1
        assert self.RedisSetMock().__enter__().setex.call_count == 1
        self.RedisSetMock().__enter__().setex.assert_called_once_with(
            '{"__module__": "unittest.mock", "__qualname__": "MagicMock", "args": [], "kwargs": {}}',
            ttl,
            '{"test_key": "test_value"}',
        )

    @patch("apps.utils.helpers.StrictRedis.from_url", side_effect=ConnectionError)
    def test_redis_is_unreachable_and_actual_function_gets_called(self, *args):
        decorated_func = redis_cache(redis_url="redis://test")(self.func)
        result = decorated_func()

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1

    @patch("apps.utils.helpers.StrictRedis.from_url", side_effect=RedisGetMock)
    def test_redis_recaches_value_when_update_redis_cache_is_set_to_true(self, *args):
        decorated_func = redis_cache(redis_url="redis://test")(self.func)
        result = decorated_func(update_redis_cache=True)

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1
        assert self.RedisGetMock().__enter__().get.call_count == 0
        assert self.RedisGetMock().__enter__().setex.call_count == 1
        self.RedisGetMock().__enter__().setex.assert_called_once_with(
            '{"__module__": "unittest.mock", "__qualname__": "MagicMock", "args": [], "kwargs": {}}',
            settings.REDIS_CACHE_DEFAULT_TTL,
            '{"test_key": "test_value"}',
        )

    def test_redis_cache_decorator_works_without_parameters(self, *args):
        decorated_func = redis_cache(self.func)
        result = decorated_func()

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1

    def test_redis_cache_decorator_works_with_parameters(self, *args):
        decorated_func = redis_cache()(self.func)
        result = decorated_func()

        assert result == self.EXPECTED_RESULT
        assert self.func.call_count == 1
