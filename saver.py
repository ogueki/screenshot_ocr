import os, datetime
from PIL import Image
from config import SAVE_DIR

# 保存ディレクトリの準備
os.makedirs(SAVE_DIR, exist_ok=True)


def save_files(img: Image.Image, text: str) -> None:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(SAVE_DIR, f"screenshot_{ts}.png")
    txt_path = os.path.join(SAVE_DIR, f"screenshot_{ts}.txt")
    img.save(img_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✔] {img_path}\n[✔] {txt_path}")