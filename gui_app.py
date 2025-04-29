import threading
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pyautogui

from ocr_utils import capture_and_ocr
from saver import save_files

class OCRGui(tk.Tk):
    def __init__(self, api_key_available=True):
        super().__init__()
        self.title("スクショ OCR ツール")
        
        # APIキーの有無を保存
        self.api_key_available = api_key_available

        self.mode_ocr = tk.StringVar(value="normal")
        frm_ocr = ttk.LabelFrame(self, text="OCR モード", padding=10)
        frm_ocr.pack(padx=10, pady=10, fill="x")
        ttk.Radiobutton(frm_ocr, text="通常 (Tesseract)", variable=self.mode_ocr, value="normal").pack(anchor="w")
        
        self.rb_high = ttk.Radiobutton(frm_ocr, text="高機能 (GPT-4 Vision)", variable=self.mode_ocr, value="high")
        self.rb_high.pack(anchor="w")
        
        # APIキーがない場合は高機能モードを無効化
        if not self.api_key_available:
            self.rb_high.configure(state="disabled")
            # APIキーがない場合の警告表示
            ttk.Label(frm_ocr, text="※ OpenAI APIキーが設定されていないため、高機能モードは使用できません", 
                     foreground="red").pack(anchor="w", pady=(0, 5))
        
        # モード適用ボタン
        self.btn_apply = ttk.Button(frm_ocr, text="モード適用", command=self.apply_mode)
        self.btn_apply.pack(anchor="w", pady=(5, 0))

        self.status = tk.StringVar(value="モード未選択")
        ttk.Label(self, textvariable=self.status).pack(padx=10, pady=(0, 10))
        
        # 現在のモード表示
        self.current_mode = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.current_mode).pack(padx=10, pady=(0, 10))

        # ボタンフレーム
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # 終了ボタン（右寄せ）
        ttk.Button(frm_buttons, text="終了", command=self.quit_all).pack(side="right")

        self._busy = False
        self._hooked = False

    # モード適用メソッド
    def apply_mode(self):
        if self._hooked:
            keyboard.unhook_all_hotkeys()
            self._hooked = False
            self.register_hotkey()
        else:
            self.register_hotkey()

    def register_hotkey(self):
        if self._hooked:
            return

        def on_prtsc():
            if self._busy:
                return
            self._busy = True
            threading.Thread(target=self._run_capture, daemon=True).start()

        keyboard.add_hotkey("print_screen", on_prtsc, suppress=False)
        self._hooked = True
        
        # モード表示の更新
        mode_text = "高機能" if self.mode_ocr.get() == "high" else "通常"
        self.status.set("登録済み。PrintScreen を押してください。")
        self.current_mode.set(f"起動中：{mode_text}モード")

    def _run_capture(self):
        try:
            img = pyautogui.screenshot()
            text = capture_and_ocr(img, self.mode_ocr.get())
            save_files(img, text)
        except Exception as e:
            self.after(0, messagebox.showerror, "エラー", str(e))
        finally:
            self._busy = False

    def quit_all(self):
        keyboard.unhook_all_hotkeys()
        self.destroy()
