from PIL import Image, ImageEnhance
import io, base64
import pytesseract

from config import TESSERACT_CMD, TESSDATA_PREFIX, BINARY_THRESHOLD, CONTRAST_FACTOR, MAX_IMAGE_SIZE, VISION_MODEL
import openai

# Tesseract の設定
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
import os
os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX

def capture_and_ocr(img: Image.Image, mode: str) -> str:
    if mode == "high" and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OpenAI APIキーが設定されていないため、高機能モードは使用できません")
    return ocr_high(img) if mode == "high" else ocr_normal(img)

# 通常モード
def ocr_normal(img: Image.Image) -> str:
    gray = img.convert("L")
    contrast = ImageEnhance.Contrast(gray).enhance(CONTRAST_FACTOR)
    return pytesseract.image_to_string(contrast, lang="jpn+eng")

# 高機能モード
def ocr_high(img: Image.Image) -> str:
    # サイズ制限
    if max(img.size) > MAX_IMAGE_SIZE:
        img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    # GPT-4 Visionへの指示
    resp = openai.OpenAI().chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "system", "content": "You are an OCR assistant. Transcribe visible text exactly; if unreadable respond NO_TEXT."},
            {"role": "user", "content": [
                {"type": "text", "text": "画像内の文字を抽出してください。説明は不要です。"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}}
            ]}
        ],
        max_tokens=4096,
    )

    choice = resp.choices[0]
    if choice.finish_reason == "content_filter":
        raise RuntimeError("OpenAI Vision refused to process this image (content_filter)")
    return choice.message.content.strip()
