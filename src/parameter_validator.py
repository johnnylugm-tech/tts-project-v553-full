#!/usr/bin/env python3
"""
Parameter Validator - 參數驗證器
===========================
依據 methodology-v2 規範實作
- 參數範圍驗證
- 類型檢查

對應規格：P1-F1.3, P1-F1.4 (rate/volume 參數)
"""

import re
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ParameterValidator:
    """
    參數驗證器
    
    對應 methodology-v2 規範：
    - SKILL.md - Validation
    - SKILL.md - Data Integrity
    """
    
    # 參數範圍定義
    RATE_RANGE = (-50, 100)  # -50% to +100%
    VOLUME_RANGE = (-50, 50)  # -50% to +50%
    
    VOICE_PATTERN = re.compile(r'^[a-zA-Z]+-[A-Z]{2}-[A-Za-z]+Neural$')
    
    @classmethod
    def validate_voice(cls, voice: str) -> Tuple[bool, Optional[str]]:
        """驗證音色"""
        if not voice:
            return False, "Voice cannot be empty"
        
        if not cls.VOICE_PATTERN.match(voice):
            return False, f"Invalid voice format: {voice}"
        
        return True, None
    
    @classmethod
    def validate_rate(cls, rate: str) -> Tuple[bool, Optional[str]]:
        """驗證語速"""
        if not rate:
            return False, "Rate cannot be empty"
        
        match = re.match(r'^([+-]?)(\d+)%$', rate)
        if not match:
            return False, f"Invalid rate format: {rate}. Use +X% or -X%"
        
        sign = 1 if match.group(1) == '+' else -1
        value = int(match.group(2))
        
        if not (cls.RATE_RANGE[0] <= sign * value <= cls.RATE_RANGE[1]):
            return False, f"Rate must be between {cls.RATE_RANGE[0]}% and {cls.RATE_RANGE[1]}%"
        
        return True, None
    
    @classmethod
    def validate_volume(cls, volume: str) -> Tuple[bool, Optional[str]]:
        """驗證音量"""
        if not volume:
            return False, "Volume cannot be empty"
        
        match = re.match(r'^([+-]?)(\d+)%$', volume)
        if not match:
            return False, f"Invalid volume format: {volume}. Use +X% or -X%"
        
        sign = 1 if match.group(1) == '+' else -1
        value = int(match.group(2))
        
        if not (cls.VOLUME_RANGE[0] <= sign * value <= cls.VOLUME_RANGE[1]):
            return False, f"Volume must be between {cls.VOLUME_RANGE[0]}% and {cls.VOLUME_RANGE[1]}%"
        
        return True, None
    
    @classmethod
    def validate_all(
        cls,
        voice: str,
        rate: str,
        volume: str
    ) -> Tuple[bool, Optional[str]]:
        """驗證所有參數"""
        # 驗證音色
        valid, error = cls.validate_voice(voice)
        if not valid:
            return False, f"Voice: {error}"
        
        # 驗證語速
        valid, error = cls.validate_rate(rate)
        if not valid:
            return False, f"Rate: {error}"
        
        # 驗證音量
        valid, error = cls.validate_volume(volume)
        if not valid:
            return False, f"Volume: {error}"
        
        return True, None