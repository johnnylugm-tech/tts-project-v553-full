#!/usr/bin/env python3
"""
Text Processor - 文本處理與分段
=============================
依據 methodology-v2 規範實作
- 智能分段
- 類型提示

對應規格：P2-F2 (文本處理)
"""

import re
import os
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# 預設分段標記 - 符合規格書 P3
DEFAULT_SPLITTERS = ["。", "？", "！", "；", "\n"]
DEFAULT_MAX_LENGTH = 800


class TextProcessor:
    """
    文本處理器
    
    對應 methodology-v2 規範：
    - SKILL.md - Data Processing
    - SKILL.md - Modularity
    """
    
    def __init__(
        self,
        max_chunk_size: int = DEFAULT_MAX_LENGTH,
        splitters: Optional[List[str]] = None
    ):
        """
        初始化文本處理器
        
        對應規格：P3-F2.5 (分段長度 500-1000 字)
        """
        self.max_chunk_size = max_chunk_size
        self.splitters = splitters or DEFAULT_SPLITTERS
        logger.info(f"TextProcessor initialized: max_chunk_size={max_chunk_size}")
    
    def process(self, text: str) -> List[str]:
        """
        處理文字並分段
        
        對應規格：P2-F2 (智能分段)
        
        Algorithm:
        1. 依分段標記切割
        2. 確保不超過最大長度
        
        Returns:
            分段後的文字列表
        """
        if not text or not text.strip():
            return []
        
        # 標準化文字
        text = self._normalize_text(text)
        
        # 第一階段：依分段標記切割
        segments = self._split_by_markers(text)
        
        # 第二階段：確保每段不超過最大長度
        final_segments = []
        for segment in segments:
            if len(segment) <= self.max_chunk_size:
                final_segments.append(segment)
            else:
                final_segments.extend(self._split_long_segment(segment))
        
        logger.info(f"Text processed: {len(text)} chars -> {len(final_segments)} segments")
        return final_segments
    
    def _normalize_text(self, text: str) -> str:
        """標準化文字"""
        # 移除控制字元
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        # 將多個空白替換為單一空白
        text = re.sub(r'\s+', ' ', text)
        # 移除行首行尾空白
        text = text.strip()
        return text
    
    def _split_by_markers(self, text: str) -> List[str]:
        """依分段標記切割"""
        if not text:
            return []
        
        # 建立正則表達式
        pattern = f"([{' '.join(re.escape(s) for s in self.splitters)}])"
        parts = re.split(pattern, text)
        
        # 合併標記到前一結果
        segments = []
        current = ""
        
        for part in parts:
            if part in self.splitters:
                current += part
            elif part:
                if current:
                    segments.append(current + part)
                    current = ""
                else:
                    segments.append(part)
            else:
                if current:
                    segments.append(current)
        
        # 處理最後一個段落
        if current:
            segments.append(current)
        
        return [s for s in segments if s.strip()]
    
    def _split_long_segment(self, text: str) -> List[str]:
        """細分過長的段落"""
        segments = []
        
        # 嘗試在句號處細分
        sub_parts = re.split(r'([。？！；])', text)
        current = ""
        
        for part in sub_parts:
            if part in self.splitters:
                current += part
            elif part:
                if len(current) + len(part) <= self.max_chunk_size:
                    current += part
                else:
                    if current:
                        segments.append(current)
                    current = part
        
        if current:
            segments.append(current)
        
        return segments
    
    def load_from_file(self, file_path: str) -> str:
        """
        從檔案載入文字
        
        對應規格：P2 (文本輸入)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"Loaded {len(content)} chars from {file_path}")
        return content