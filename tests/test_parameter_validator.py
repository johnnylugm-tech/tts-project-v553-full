#!/usr/bin/env python3
"""
單元測試 - Parameter Validator
===========================
依據 methodology-v2 規範
測試覆蓋：parameter_validator.py
"""

import pytest
from parameter_validator import ParameterValidator


class TestParameterValidator:
    """Parameter Validator 測試"""
    
    def test_validate_voice_valid(self):
        """測試有效音色"""
        valid, error = ParameterValidator.validate_voice("zh-TW-HsiaoHsiaoNeural")
        assert valid is True
        assert error is None
    
    def test_validate_voice_invalid_format(self):
        """測試無效音色格式"""
        valid, error = ParameterValidator.validate_voice("invalid-voice")
        assert valid is False
        assert "Invalid voice format" in error
    
    def test_validate_voice_empty(self):
        """測試空音色"""
        valid, error = ParameterValidator.validate_voice("")
        assert valid is False
        assert "cannot be empty" in error
    
    def test_validate_rate_valid_positive(self):
        """測試有效語速（正）"""
        valid, error = ParameterValidator.validate_rate("+50%")
        assert valid is True
    
    def test_validate_rate_valid_negative(self):
        """測試有效語速（負）"""
        valid, error = ParameterValidator.validate_rate("-30%")
        assert valid is True
    
    def test_validate_rate_invalid_format(self):
        """測試無效語速格式"""
        valid, error = ParameterValidator.validate_rate("50%")
        assert valid is False
        assert "Invalid rate format" in error
    
    def test_validate_rate_out_of_range(self):
        """測試語速超出範圍"""
        valid, error = ParameterValidator.validate_rate("+200%")
        assert valid is False
        assert "must be between" in error
    
    def test_validate_volume_valid(self):
        """測試有效音量"""
        valid, error = ParameterValidator.validate_volume("+30%")
        assert valid is True
    
    def test_validate_volume_invalid(self):
        """測試無效音量"""
        valid, error = ParameterValidator.validate_volume("100%")
        assert valid is False
    
    def test_validate_all_valid(self):
        """測試全部有效"""
        valid, error = ParameterValidator.validate_all(
            "zh-TW-HsiaoHsiaoNeural", 
            "+20%", 
            "+10%"
        )
        assert valid is True
        assert error is None
    
    def test_validate_all_invalid(self):
        """測試全部無效"""
        valid, error = ParameterValidator.validate_all(
            "invalid",
            "bad",
            "worse"
        )
        assert valid is False
        assert error is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
