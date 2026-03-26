# Phase 2: 架構設計 (SAD)

> 依據 methodology-v2 規範
> 
> **日期**：2026-03-26

---

## 2.1 系統架構總覽

```
┌─────────────────────────────────────────────────────────┐
│                    CLI 入口層                          │
│                 (PresentationTTS)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Text       │ │    TTS      │ │   Audio     │
│  Processor   │ │   Engine    │ │  Converter  │
└──────────────┘ └──────────────┘ └──────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
┌───────────────────────────────────────────────────────┐
│              錯誤處理與重試層                          │
│            (RetryHandler + CircuitBreaker)           │
└───────────────────────────────────────────────────────┘
```

---

## 2.2 模組劃分

| 模組名稱 | 職責 | 對應規格 | 檔案 |
|----------|------|----------|------|
| **TTSEngine** | 語音合成核心 | P1-F1 | `tts_engine.py` |
| **TextProcessor** | 文本分段處理 | P2-F2 | `text_processor.py` |
| **AudioConverter** | 格式轉換 | P5-F4 | `audio_converter.py` |
| **RetryHandler** | 重試與熔斷 | P4-F3 | `retry_handler.py` |
| **ParameterValidator** | 參數驗證 | - | `parameter_validator.py` |
| **WebSocketServer** | 通訊接入 | P2-F3 | `websocket_server.py` |

---

## 2.3 介面定義

### TTSEngine 介面

```python
class TTSEngine(ABC):
    @abstractmethod
    async def synthesize(text: str, output_file: str) -> str: ...
    
    @staticmethod
    async def list_voices() -> List[Dict]: ...
    
    def set_parameters(rate: str, volume: str): ...
```

### TextProcessor 介面

```python
class TextProcessor:
    def __init__(max_chunk_size: int, splitters: List[str]): ...
    
    def process(text: str) -> List[str]: ...
    
    def load_from_file(file_path: str) -> str: ...
```

---

## 2.4 對應 methodology-v2 規範

| 架構層 | methodology-v2 檔案 | 說明 |
|--------|---------------------|------|
| 入口層 | SKILL.md - CLI Design | 命令列介面設計 |
| 引擎層 | SKILL.md - Core Modules | 核心模組 |
| 處理層 | SKILL.md - Data Processing | 資料處理 |
| 錯誤處理 | SKILL.md - Error Handling | 錯誤處理規範 |
| 驗證層 | SKILL.md - Validation | 參數驗證 |

---

## 2.5 Constitution Phase 2 檢查

依據 `quality_gate/constitution/sad_constitution_checker.py`：

- [x] SAD 文件存在
- [x] 系統架構圖完整
- [x] 模組職責清晰
- [x] 介面定義明確
- [x] 符合分層原則

---

## 2.6 衝突記錄 (Conflict Log)

| 時間 | 衝突點 | 解決方案 | 依據 |
|------|--------|----------|------|
| - | 無 | - | - |

---

## Phase 2 完成狀態

| 交付物 | 狀態 |
|--------|------|
| SAD 文件 | ✅ 完成 |
| 模組劃分 | ✅ 完成 |
| 介面定義 | ✅ 完成 |
| Constitution Phase 2 | ✅ 通過 |

---

**下一步**：Phase 3 實作 → 程式碼實現