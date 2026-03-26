#!/usr/bin/env python3
"""
單元測試 - TTS Engine
==================
依據 methodology-v2 規範
測試覆蓋：tts_engine.py
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from tts_engine import TTSEngine, DEFAULT_VOICE, DEFAULT_RATE, DEFAULT_VOLUME


class TestTTSEngine:
    """TTS Engine 測試"""
    
    def test_init_default(self):
        """測試預設初始化"""
        engine = TTSEngine()
        assert engine.voice == DEFAULT_VOICE
        assert engine.rate == DEFAULT_RATE
        assert engine.volume == DEFAULT_VOLUME
    
    def test_init_custom(self):
        """測試自訂參數"""
        engine = TTSEngine(voice="zh-TW-YunJingNeural", rate="+20%", volume="+10%")
        assert engine.voice == "zh-TW-YunJingNeural"
        assert engine.rate == "+20%"
        assert engine.volume == "+10%"
    
    def test_set_parameters(self):
        """測試設定參數"""
        engine = TTSEngine()
        engine.set_parameters(rate="+30%", volume="+20%")
        assert engine.rate == "+30%"
        assert engine.volume == "+20%"
    
    def test_get_parameters(self):
        """測試取得參數"""
        engine = TTSEngine(rate="+10%", volume="-10%")
        params = engine.get_parameters()
        assert params["voice"] == DEFAULT_VOICE
        assert params["rate"] == "+10%"
        assert params["volume"] == "-10%"
    
    @pytest.mark.asyncio
    async def test_synthesize_to_file(self):
        """測試合成到檔案"""
        engine = TTSEngine()
        
        with patch('edge_tts.Communicate') as mock_comm:
            mock_comm_instance = AsyncMock()
            mock_comm.return_value = mock_comm_instance
            mock_comm_instance.save = AsyncMock()
            
            result = await engine.synthesize("測試文字", "output.mp3")
            
            mock_comm.assert_called_once()
            mock_comm_instance.save.assert_called_once_with("output.mp3")
    
    @pytest.mark.asyncio
    async def test_synthesize_error(self):
        """測試合成錯誤處理"""
        engine = TTSEngine()
        
        with patch('edge_tts.Communicate') as mock_comm:
            mock_comm.side_effect = Exception("Network error")
            
            with pytest.raises(Exception) as exc_info:
                await engine.synthesize("測試", "output.mp3")
            assert "Network error" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
