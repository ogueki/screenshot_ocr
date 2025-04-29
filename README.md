# スクリーンショットOCRツール

スクリーンショットを撮るだけで、画像内の文字を自動で抽出し、テキストとして保存するOCRツールです。

-  通常モード：Tesseract OCR（無料）
-  高機能モード：GPT-4 Vision（OpenAI APIキーが必要）

---

## 機能一覧

- ツール起動中、PrintScreenキーで自動スクショ＋OCR
- OCR結果を `.txt` で保存
- スクリーンショット画像も一緒に保存
- Tesseract または GPT-4 Vision から選べる

---

##  対応環境

- Windows 10 / 11
- Python 3.10 以上（推奨）

---

##  インストール手順

### 1. リポジトリをクローン

### 2. 必要なライブラリをインストール
pip install -r requirements.txt
### 3. Tesseract OCR のインストール（未導入の場合）
以下からインストーラをダウンロードして実行：

🔗 https://github.com/tesseract-ocr/tesseract

インストール後、次のようなパスにあることを確認してください：

C:\Program Files\Tesseract-OCR\tesseract.exe

# 使い方
main.py を実行

python main.py
GUIが起動したら、OCRモードを選択して「モード適用」ボタンを押してください

PrintScreen キーを押すとスクリーンショットが撮影され、OCRが実行されます

imgフォルダに画像とテキストファイルが保存されます

# GPT-4 Vision モードを使うには
OpenAI APIキーが必要です。環境変数 OPENAI_API_KEY を設定してください。

