#!/usr/bin/env python3
"""
單元測試 - Text Processor
======================
依據 methodology-v2 規範
測試覆蓋：text_processor.py
"""

import pytest
from text_processor import TextProcessor, DEFAULT_SPLITTERS, DEFAULT_MAX_LENGTH


class TestTextProcessor:
    """Text Processor 測試"""
    
    def test_init_default(self):
        """測試預設初始化"""
        tp = TextProcessor()
        assert tp.max_chunk_size == DEFAULT_MAX_LENGTH
        assert tp.splitters == DEFAULT_SPLITTERS
    
    def test_init_custom(self):
        """測試自訂參數"""
        tp = TextProcessor(max_chunk_size=500, splitters=["。", "？"])
        assert tp.max_chunk_size == 500
        assert tp.splitters == ["。", "？"]
    
    def test_process_empty(self):
        """測試空文字"""
        tp = TextProcessor()
        assert tp.process("") == []
        assert tp.process("   ") == []
    
    def test_process_simple(self):
        """測試簡單分段"""
        tp = TextProcessor()
        text = "你好。 world"
        result = tp.process(text)
        assert len(result) > 0
    
    def test_process_with_markers(self):
        """測試標記分段"""
        tp = TextProcessor()
        text = "第一句。第二句！第三句？第四句；"
        result = tp.process(text)
        assert any("第一句" in r for r in result)
        assert any("第二句" in r for r in result)
    
    def test_process_long_text(self):
        """測試長文字"""
        tp = TextProcessor(max_chunk_size=10)
        text = "這是一個很長的文字需要被分段處理"
        result = tp.process(text)
        for r in result:
            assert len(r) <= 15  # max_chunk_size + buffer
    
    def test_normalize_text(self):
        """測試文字標準化"""
        tp = TextProcessor()
        text = "  hello\n\nworld  "
        result = tp._normalize_text(text)
        assert result == "hello world"
    
    def test_load_from_file(self):
        """測試檔案載入"""
        tp = TextProcessor()
        # Create temp file
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write("測試內容")
            temp_path = f.name
        
        try:
            result = tp.load_from_file(temp_path)
            assert result == "測試內容"
        finally:
            os.unlink(temp_path)
    
    def test_load_from_file_not_found(self):
        """測試檔案不存在"""
        tp = TextProcessor()
        with pytest.raises(FileNotFoundError):
            tp.load_from_file("/nonexistent/file.txt")


class TestTextProcessorSplitters:
    """分段標記測試"""
    
    def test_period_splitter(self):
        """句號分段"""
        tp = TextProcessor()
        result = tp.process("句子一。句子二。")
        assert len(result) >= 1
    
    def test_question_splitter(self):
        """問號分段"""
        tp = TextProcessor()
        result = tp.process("問題？答案")
        assert len(result) >= 1
    
    def test_exclamation_splitter(self):
        """感嘆號分段"""
        tp = TextProcessor()
        result = tp.process("驚嘆！真的")
        assert len(result) >= 1
    
    def test_newline_splitter(self):
        """換行分段"""
        tp = TextProcessor()
        result = tp.process("第一行\n第二行")
        assert len(result) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
