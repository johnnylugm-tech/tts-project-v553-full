#!/usr/bin/env python3
"""
Audio Converter - 音訊格式轉換
============================
依據 methodology-v2 規範實作
- ffmpeg 整合
- 格式轉換

對應規格：P5-F4.2 (WAV 輸出)
"""

import subprocess
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AudioConverter:
    """
    音訊格式轉換器
    
    對應 methodology-v2 規範：
    - SKILL.md - Data Processing
    """
    
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg_path = ffmpeg_path
    
    def mp3_to_wav(self, input_file: str, output_file: Optional[str] = None) -> Optional[str]:
        """
        MP3 轉 WAV
        
        對應規格：P5-F4.2
        """
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return None
        
        if output_file is None:
            output_file = os.path.splitext(input_file)[0] + ".wav"
        
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-i", input_file, "-y", output_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info(f"Converted: {output_file}")
                return output_file
            else:
                logger.error(f"Conversion failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Conversion timeout")
            return None
        except FileNotFoundError:
            logger.error(f"ffmpeg not found: {self.ffmpeg_path}")
            return None
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return None
    
    def is_available(self) -> bool:
        """檢查 ffmpeg 是否可用"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False


def convert_to_wav(input_file: str, output_file: Optional[str] = None) -> Optional[str]:
    """便捷函數"""
    converter = AudioConverter()
    return converter.mp3_to_wav(input_file, output_file)