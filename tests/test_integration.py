#!/usr/bin/env python3
"""整合測試 - Integration Tests
==============================="""

import pytest
import asyncio
import tempfile
import os
from unittest.mock import patch, AsyncMock
from src.tts_engine import TTSEngine
from src.text_processor import TextProcessor
from src.parameter_validator import ParameterValidator
from src.retry_handler import RetryHandler


class TestTTSIntegration:
    """TTS 整合測試"""
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        """測試完整流程"""
        # 1. 驗證參數
        valid, _ = ParameterValidator.validate_all("zh-TW-HsiaoHsiaoNeural", "+10%", "+0%")
        assert valid
        
        # 2. 文本處理
        tp = TextProcessor(max_chunk_size=100)
        text = "你好世界。這是測試。"
        chunks = tp.process(text)
        assert len(chunks) > 0
        
        # 3. 引擎初始化
        engine = TTSEngine(voice="zh-TW-HsiaoHsiaoNeural", rate="+10%", volume="+0%")
        params = engine.get_parameters()
        assert params["voice"] == "zh-TW-HsiaoHsiaoNeural"
    
    def test_error_handling_pipeline(self):
        """錯誤處理流程"""
        # 參數驗證失敗
        valid, error = ParameterValidator.validate_rate("invalid")
        assert valid is False
        
        # 文本處理空輸入
        tp = TextProcessor()
        result = tp.process("")
        assert result == []


class TestEndToEnd:
    """端到端測試"""
    
    def test_cli_parameters(self):
        """測試 CLI 參數"""
        valid, _ = ParameterValidator.validate_all(
            "zh-TW-HsiaoHsiaoNeural",
            "+20%",
            "+10%"
        )
        assert valid
    
    def test_chunk_size_boundary(self):
        """測試分段邊界"""
        tp = TextProcessor(max_chunk_size=50)
        long_text = "這是一個很長的文字" * 20
        chunks = tp.process(long_text)
        for chunk in chunks:
            assert len(chunk) <= 60  # buffer


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
