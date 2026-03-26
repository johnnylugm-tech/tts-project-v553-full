#!/usr/bin/env python3
"""
Retry Handler - 重試機制與熔斷器
==============================
依據 methodology-v2 規範實作
- 指數退避
- 熔斷器狀態機
- 錯誤處理

對應規格：P4-F3 (錯誤重試機制)
"""

import asyncio
import time
from typing import TypeVar, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_DELAY = 1


class CircuitState(Enum):
    """熔斷器狀態"""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """熔斷器實作"""
    failure_threshold: int = 5
    recovery_timeout: float = 60
    success_threshold: int = 2
    
    _failure_count: int = field(default=0, init=False)
    _success_count: int = field(default=0, init=False)
    _last_failure_time: float = field(default=0, init=False)
    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)
    
    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                return CircuitState.HALF_OPEN
        return self._state
    
    async def call(self, coro_func: Callable, *args, **kwargs) -> Any:
        async with self._lock:
            current_state = self.state
            
            if current_state == CircuitState.OPEN:
                raise Exception(f"Circuit breaker OPEN")
            
            try:
                result = await coro_func(*args, **kwargs)
                if current_state == CircuitState.HALF_OPEN:
                    self._success_count += 1
                    if self._success_count >= self.success_threshold:
                        self._reset()
                else:
                    self._failure_count = 0
                return result
            except Exception as e:
                self._record_failure()
                raise e
    
    def _record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
    
    def _reset(self):
        self._failure_count = 0
        self._success_count = 0
        self._state = CircuitState.CLOSED


class RetryHandler:
    """
    重試處理器
    
    對應 methodology-v2 規範：
    - SKILL.md - Error Handling
    - SKILL.md - Resilience
    """
    
    def __init__(
        self,
        max_retries: int = DEFAULT_MAX_RETRIES,
        base_delay: float = DEFAULT_BASE_DELAY
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def calculate_delay(self, attempt: int) -> float:
        """
        指數退避計算
        
        對應規格：P4-F3 (指數退避策略)
        """
        return self.base_delay * (2 ** attempt)
    
    async def execute_with_retry(
        self,
        coro_func: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """
        執行帶重試
        
        對應規格：P4-F3.1 (錯誤重試機制)
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await coro_func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.calculate_delay(attempt)
                    logger.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
        
        logger.error(f"All {self.max_retries} attempts failed")
        raise last_exception
    
    async def execute_with_circuit_breaker(
        self,
        coro_func: Callable[..., Any],
        *args,
        failure_threshold: int = 5,
        recovery_timeout: float = 60,
        success_threshold: int = 2,
        **kwargs
    ) -> Any:
        """執行帶熔斷器"""
        cb = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            success_threshold=success_threshold
        )
        return await cb.call(coro_func, *args, **kwargs)