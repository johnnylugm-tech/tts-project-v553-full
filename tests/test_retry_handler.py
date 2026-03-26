#!/usr/bin/env python3
"""
單元測試 - Retry Handler
====================
依據 methodology-v2 規範
測試覆蓋：retry_handler.py
"""

import pytest
import asyncio
from unittest.mock import AsyncMock
from retry_handler import RetryHandler, CircuitBreaker, CircuitState


class TestRetryHandler:
    """Retry Handler 測試"""
    
    def test_init_default(self):
        """測試預設初始化"""
        handler = RetryHandler()
        assert handler.max_retries == 3
        assert handler.base_delay == 1
    
    def test_init_custom(self):
        """測試自訂參數"""
        handler = RetryHandler(max_retries=5, base_delay=2)
        assert handler.max_retries == 5
        assert handler.base_delay == 2
    
    def test_calculate_delay(self):
        """測試指數退避"""
        handler = RetryHandler()
        assert handler.calculate_delay(0) == 1
        assert handler.calculate_delay(1) == 2
        assert handler.calculate_delay(2) == 4
        assert handler.calculate_delay(3) == 8
    
    @pytest.mark.asyncio
    async def test_execute_with_retry_success(self):
        """測試重試成功"""
        handler = RetryHandler()
        mock_func = AsyncMock(return_value="success")
        
        result = await handler.execute_with_retry(mock_func)
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    @pytest.mark.asyncio
    async def test_execute_with_retry_eventual_success(self):
        """測試最終成功"""
        handler = RetryHandler(max_retries=3, base_delay=0)
        mock_func = AsyncMock(side_effect=[Exception("fail"), "success"])
        
        result = await handler.execute_with_retry(mock_func)
        
        assert result == "success"
        assert mock_func.call_count == 2
    
    @pytest.mark.asyncio
    async def test_execute_with_retry_all_fail(self):
        """測試全部失敗"""
        handler = RetryHandler(max_retries=2, base_delay=0)
        mock_func = AsyncMock(side_effect=Exception("always fail"))
        
        with pytest.raises(Exception) as exc_info:
            await handler.execute_with_retry(mock_func)
        
        assert mock_func.call_count == 2


class TestCircuitBreaker:
    """Circuit Breaker 測試"""
    
    def test_init_default(self):
        """測試預設初始化"""
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_call_success(self):
        """測試呼叫成功"""
        cb = CircuitBreaker()
        mock_func = AsyncMock(return_value="success")
        
        result = await cb.call(mock_func)
        
        assert result == "success"
        assert cb.state == CircuitState.CLOSED
    
    @pytest.mark.asyncio
    async def test_call_failure_opens_circuit(self):
        """測試失敗打開熔斷"""
        cb = CircuitBreaker(failure_threshold=2)
        mock_func = AsyncMock(side_effect=Exception("fail"))
        
        with pytest.raises(Exception):
            await cb.call(mock_func)
        
        # First failure doesn't open yet
        assert cb.state == CircuitState.CLOSED
        
        with pytest.raises(Exception):
            await cb.call(mock_func)
        
        # Second failure opens
        assert cb.state == CircuitState.OPEN
    
    @pytest.mark.asyncio
    async def test_open_rejects_calls(self):
        """測試開路狀態拒絕呼叫"""
        cb = CircuitBreaker(failure_threshold=1)
        mock_func = AsyncMock(side_effect=Exception("fail"))
        
        with pytest.raises(Exception):
            await cb.call(mock_func)
        
        # Now open
        assert cb.state == CircuitState.OPEN
        
        # Next call should be rejected
        with pytest.raises(Exception) as exc_info:
            await cb.call(mock_func)
        
        assert "Circuit breaker OPEN" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
