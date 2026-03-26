#!/usr/bin/env python3
"""Audio Converter Tests - methodology-v2"""

import pytest, os, tempfile
from unittest.mock import patch, Mock
from audio_converter import AudioConverter, convert_to_wav

class TestAudioConverter:
    def test_init_default(self):
        c = AudioConverter()
        assert c.ffmpeg_path == "ffmpeg"
    
    @patch('subprocess.run')
    def test_is_available_true(self, m):
        m.return_value = Mock(returncode=0)
        c = AudioConverter()
        assert c.is_available() is True
    
    @patch('subprocess.run')
    def test_is_available_false(self, m):
        m.side_effect = FileNotFoundError()
        c = AudioConverter()
        assert c.is_available() is False
    
    @patch('subprocess.run')
    def test_mp3_to_wav_success(self, m):
        m.return_value = Mock(returncode=0)
        c = AudioConverter()
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            inp, out = f.name, f.name.replace('.mp3', '.wav')
        try:
            r = c.mp3_to_wav(inp, out)
            assert r == out
        finally:
            [os.unlink(p) for p in [inp, out] if os.path.exists(p)]

if __name__ == "__main__": pytest.main([__file__, "-v"])