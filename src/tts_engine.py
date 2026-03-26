#!/usr/bin/env python3
"""
TTS Engine - Edge TTS 語音合成引擎
==================================
依據 methodology-v2 規範實作
- 模組解耦
- 錯誤處理
- 類型提示

對應規格：P1-F1 (語音合成)
"""

import asyncio
import edge_tts
from typing import AsyncIterator, Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

# 預設音色 - 符合規格書 P1
DEFAULT_VOICE = "zh-TW-HsiaoHsiaoNeural"
DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"


class TTSEngine:
    """
    TTS 引擎 - 語音合成核心
    
    對應 methodology-v2 規範：
    - SKILL.md - Core Modules
    - SKILL.md - Error Handling
    """
    
    def __init__(
        self,
        voice: str = DEFAULT_VOICE,
        rate: str = DEFAULT_RATE,
        volume: str = DEFAULT_VOLUME
    ):
        """
        初始化 TTS 引擎
        
        對應規格：P1-F1.3, P1-F1.4 (rate/volume 參數)
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        logger.info(f"TTSEngine initialized: voice={voice}, rate={rate}, volume={volume}")
    
    async def synthesize(
        self,
        text: str,
        output_file: Optional[str] = None
    ) -> Optional[str]:
        """
        合成文字為語音
        
        對應規格：P1-F1 (語音合成)
        
        Args:
            text: 要合成的文字
            output_file: 輸出檔案路徑
            
        Returns:
            輸出檔案路徑或音訊資料
        """
        try:
            if output_file:
                # 儲存到檔案 - 符合 methodology-v2 Error Handling
                communicate = edge_tts.Communicate(
                    text, 
                    self.voice, 
                    rate=self.rate, 
                    volume=self.volume
                )
                await communicate.save(output_file)
                logger.info(f"Audio saved to: {output_file}")
                return output_file
            else:
                # 返回音訊資料 - 流式處理
                chunks = []
                communicate = edge_tts.Communicate(
                    text, 
                    self.voice, 
                    rate=self.rate, 
                    volume=self.volume
                )
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        chunks.append(chunk["data"])
                return b"".join(chunks)
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            raise
    
    async def synthesize_stream(
        self,
        text: str
    ) -> AsyncIterator[bytes]:
        """
        流式合成
        
        對應規格：P2-F3 (WebSocket 流式傳輸)
        """
        communicate = edge_tts.Communicate(
            text, 
            self.voice, 
            rate=self.rate, 
            volume=self.volume
        )
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]
    
    @staticmethod
    async def list_voices() -> List[Dict[str, str]]:
        """
        取得可用語音列表
        
        對應規格：P1-F1.2 (音色選擇)
        """
        voices = await edge_tts.list_voices()
        # 過濾中文語音
        return [v for v in voices if v["Locale"].startswith("zh-")]
    
    def set_parameters(self, rate: Optional[str] = None, volume: Optional[str] = None):
        """
        設定參數
        
        對應規格：P1-F1.3, P1-F1.4
        """
        if rate is not None:
            self.rate = rate
        if volume is not None:
            self.volume = volume
        logger.info(f"Parameters updated: rate={self.rate}, volume={self.volume}")
    
    def get_parameters(self) -> Dict[str, str]:
        """取得目前參數"""
        return {
            "voice": self.voice,
            "rate": self.rate,
            "volume": self.volume
        }