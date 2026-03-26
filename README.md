# TTS 簡報配音系統

> 基於 edge-tts 之高品質簡報配音系統
> 依據 methodology-v2 規範實作

## 功能特點

- 🎙️ **Microsoft Edge TTS** - 高品質神經網路語音
- 🗣️ **台灣國語音色** - zh-TW-HsiaoHsiaoNeural
- ⚡ **非同步架構** - asyncio + WebSocket 流式傳輸
- 🔄 **智能分段** - 句號、問號、感嘆號、換行符
- 🛡️ **錯誤處理** - 重試機制 + 熔斷器
- ✅ **完整測試** - 單元測試 + 整合測試

## 安裝

```bash
pip install -r requirements.txt
```

## 使用方式

```bash
# 基本使用
python -m src.cli "Hello World" -o output.mp3

# 使用文字檔
python -m src.cli input.txt -o output.mp3

# 調整參數
python -m src.cli "測試" -v zh-TW-HsiaoHsiaoNeural -r "+20%" --volume "+10%"

# 輸出 WAV
python -m src.cli "測試" -o output.wav -f wav

# 列出可用音色
python -m src.cli --list-voices
```

## 專案結構

```
tts-v553-full/
├── src/
│   ├── tts_engine.py         # 語音合成引擎
│   ├── text_processor.py     # 文本處理
│   ├── parameter_validator.py # 參數驗證
│   ├── retry_handler.py      # 重試+熔斷
│   ├── audio_converter.py    # 格式轉換
│   └── cli.py               # 命令列介面
├── tests/                    # 測試檔案
├── 01-specify/              # SRS 需求規格
├── 02-plan/                 # SAD 架構設計
└── SPEC_TRACKING.md         # 規格追蹤
```

## 執行測試

```bash
pytest tests/ -v
```

## 技術規格

| 項目 | 規格 |
|------|------|
| Python | 3.8+ |
| 核心庫 | edge-tts |
| 預設音色 | zh-TW-HsiaoHsiaoNeural |
| 分段長度 | 500-1000 字元 |
| 輸出格式 | MP3, WAV |

## License

MIT

---

**依據 methodology-v2 規範實作**