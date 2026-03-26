# SPEC_TRACKING.md - 規格書 vs 實作對照表

> 零偏差參照規格書
> 
> **更新日期**：2026-03-26

---

## 📋 對照表

### 核心功能

| 規格頁碼 | 規格要求 | 實作檔案 | 狀態 | 備註 |
|----------|----------|----------|------|------|
| P1 | zh-TW-HsiaoHsiaoNeural 音色 | tts_engine.py:16 | ✅ | |
| P1 | rate 參數控制 (+/-X%) | tts_engine.py:28-33 | ✅ | 含驗證 |
| P1 | volume 參數控制 (+/-X%) | tts_engine.py:28-33 | ✅ | 含驗證 |
| P2 | asyncio 非同步框架 | tts_engine.py, cli.py | ✅ | |
| P2 | WebSocket 流式傳輸 | tts_engine.py:55-62 | ✅ | |
| P3 | 句號（。）分段 | text_processor.py:16 | ✅ | |
| P3 | 問號（？）分段 | text_processor.py:16 | ✅ | |
| P3 | 感嘆號（！）分段 | text_processor.py:16 | ✅ | |
| P3 | 換行符分段 | text_processor.py:16 | ✅ | |
| P3 | 分段長度 500-1000 字 | text_processor.py:17, cli.py:27 | ✅ | 預設800 |
| P4 | 錯誤重試機制 | retry_handler.py:78-98 | ✅ | |
| P4 | 指數退避策略 | retry_handler.py:60-65 | ✅ | 2**attempt |
| P5 | MP3 輸出 | cli.py:56-65 | ✅ | |
| P5 | WAV 輸出 | audio_converter.py:22-48 | ✅ | |
| P5 | 錯誤日誌記錄 | 全專案 logging | ✅ | |

---

## 🔄 更新紀錄

| 日期 | 更新內容 |
|------|----------|
| 2026-03-26 | Phase 3 實作完成，15/15 項目 ✅ |

---

## ✅ 驗收清單

- [x] 所有項目從 ⬜ 變為 ✅