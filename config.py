# 各種設定を集中管理するモジュール
import os

# Tesseract のパス（必要に応じて変更）
TESSERACT_CMD = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSDATA_PREFIX = r"C:\\Program Files\\Tesseract-OCR\\tessdata"

# 保存ディレクトリ
SAVE_DIR = os.getenv("OCR_SAVE_DIR", "img")

# 二値化の閾値
BINARY_THRESHOLD = int(os.getenv("OCR_BINARY_THRESHOLD", 180))
# コントラスト強調の倍率
CONTRAST_FACTOR = float(os.getenv("OCR_CONTRAST_FACTOR", 1.5))

# GPT Vision 用モデル
VISION_MODEL = os.getenv("OCR_VISION_MODEL", "gpt-4o")

# 画像の最大サイズ (長辺)
MAX_IMAGE_SIZE = int(os.getenv("OCR_MAX_IMG", 2048))
