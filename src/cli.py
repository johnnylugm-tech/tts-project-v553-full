#!/usr/bin/env python3
"""
CLI - 命令列介面
================
依據 methodology-v2 規範實作
"""

import argparse
import asyncio
import os
import sys
import logging
from tts_engine import TTSEngine
from text_processor import TextProcessor
from parameter_validator import ParameterValidator
from retry_handler import RetryHandler
from audio_converter import AudioConverter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_VOICE = "zh-TW-HsiaoHsiaoNeural"
DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"
TEMP_DIR = "temp_tts_segments"

class PresentationTTS:
    def __init__(self, voice=DEFAULT_VOICE, rate=DEFAULT_RATE, volume=DEFAULT_VOLUME, chunk_size=800):
        valid, error = ParameterValidator.validate_all(voice, rate, volume)
        if not valid: raise ValueError(f"Validation failed: {error}")
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.text_processor = TextProcessor(max_chunk_size=chunk_size)
        self.tts_engine = TTSEngine(voice=voice, rate=rate, volume=volume)
        self.retry_handler = RetryHandler()
    
    async def run(self, input_source: str, output_file: str) -> bool:
        try:
            if os.path.isfile(input_source) and input_source.endswith('.txt'):
                content = self.text_processor.load_from_file(input_source)
            else:
                content = input_source
            chunks = self.text_processor.process(content)
            if not chunks: return False
            os.makedirs(TEMP_DIR, exist_ok=True)
            temp_files = []
            for i, chunk in enumerate(chunks):
                output_path = os.path.join(TEMP_DIR, f"chunk_{i:03d}.mp3")
                try:
                    await self.retry_handler.execute_with_retry(self.tts_engine.synthesize, chunk, output_path)
                    temp_files.append(output_path)
                except Exception as e: logger.error(f"Chunk {i} failed: {e}")
            if not temp_files: return False
            with open(output_file, "wb") as final_audio:
                for temp_file in temp_files:
                    with open(temp_file, "rb") as f: final_audio.write(f.read())
            for f in temp_files:
                try: os.remove(f)
                except: pass
            logger.info(f"Completed: {output_file}")
            return True
        except Exception as e: logger.error(f"Error: {e}"); return False

def parse_args():
    parser = argparse.ArgumentParser(description="TTS 簡報配音系統")
    parser.add_argument("input")
    parser.add_argument("-o", "--output", default="output.mp3")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE)
    parser.add_argument("-r", "--rate", default=DEFAULT_RATE)
    parser.add_argument("--volume", default=DEFAULT_VOLUME)
    parser.add_argument("-c", "--chunk-size", type=int, default=800)
    parser.add_argument("--list-voices", action="store_true")
    parser.add_argument("-f", "--format", choices=["mp3", "wav"], default="mp3")
    return parser.parse_args()

async def main():
    args = parse_args()
    if args.list_voices:
        voices = await TTSEngine.list_voices()
        print("可用音色:", [v.get('Name','Unknown') for v in voices[:20]])
        return
    print("=" * 50, "\nTTS 簡報配音系統\n" + "=" * 50)
    mp3_output = args.output if args.format == "mp3" or args.output.endswith(".wav") else args.output
    tts = PresentationTTS(voice=args.voice, rate=args.rate, volume=args.volume, chunk_size=args.chunk_size)
    success = await tts.run(args.input, mp3_output)
    if success:
        if args.format == "wav":
            converter = AudioConverter()
            wav_output = converter.mp3_to_wav(mp3_output, args.output.replace(".mp3",".wav") if ".mp3" in args.output else args.output)
            print(f"{'✅ 完成' if wav_output else '❌ 失敗'}: {wav_output or args.output}")
        else: print(f"✅ 完成: {args.output}")
    else: print("❌ 失敗"); sys.exit(1)

if __name__ == "__main__": asyncio.run(main())