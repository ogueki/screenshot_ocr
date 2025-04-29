import os
import sys
from gui_app import OCRGui

if __name__ == "__main__":
    # APIキーの有無を確認
    api_key_available = bool(os.getenv("OPENAI_API_KEY"))
    
    # APIキーの有無をGUIに伝えてアプリを起動
    app = OCRGui(api_key_available=api_key_available)
    app.mainloop()
