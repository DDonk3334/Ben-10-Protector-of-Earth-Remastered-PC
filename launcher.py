import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import sys
import time
from backend import BASE_DIR, ConfigManager

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(BASE_DIR, rel_path)


LANGS = {
    "en": {
        "sub": "REMASTERED PC  |  60 FPS WIDESCREEN",
        "time": "PLAYTIME: {h}h {m}m",
        "tabs": ("  PLAY  ", "  SETTINGS  ", "  CONTROLS  "),
        "gdata": "GAME DATA FILE (.ISO / .CSO)",
        "sel": "SELECT FILE",
        "norom": "No game file selected (.iso / .cso)",
        "load": "Loaded: ",
        "mods": "MODS:",
        "addm": "+ INSTALL MOD",
        "clrm": "CLEAR",
        "warn": "⚠ Warning: Mods/cheats may break the game. Use stable PSP mods.",
        "play": "▶  PLAY GAME",
        "run": "RUNNING...",
        "inp": "INPUT PROFILE",
        "kb": "Keyboard + Mouse (WASD + Click Attacks)",
        "gp": "Xbox / PlayStation Controller (XInput)",
        "res": "RENDER RESOLUTION",
        "nat": "Native",
        "perf": "PERFORMANCE & DISPLAY",
        "fps": "Unlock 60 FPS Mode (Recommended)",
        "low": "Low-End / Old PC Mode (Native Res & Fast Speed)",
        "fs": "Fullscreen Mode (16:9 Widescreen)",
        "vs": "Enable VSync",
        "sav": "SAVES:",
        "bkp": "BACKUP",
        "rsts": "RESTORE",
        "bkpok": "Saved to SaveStates_Backup.zip!",
        "rstok": "Save states restored!",
        "rstno": "SaveStates_Backup.zip not found.",
        "art": "ART:",
        "csta": "CUSTOM",
        "rsta": "RESET",
        "modok": "Mod installed: ",
        "clrask": "Remove all mods and restore original files?",
        "clrok": "All mods removed!",
        "norom_w": "Select your game image (.iso / .cso) first!",
        "keys": [
            ("W A S D", "Move Character"),
            ("SPACEBAR", "Jump / Double Jump"),
            ("LMB / J", "Light Attack"),
            ("RMB / K", "Heavy Attack"),
            ("SHIFT / L", "Block / Grab / Interact"),
            ("1-4 / ARROWS", "Select Alien Form"),
            ("Q / E", "Omnitrix / Camera"),
            ("F5 / F7", "Quick Save / Load State"),
            ("ESC / TAB", "Pause / Upgrades")
        ]
    },
    "ru": {
        "sub": "REMASTERED PC  |  60 FPS ШИРОКИЙ ЭКРАН",
        "time": "В ИГРЕ: {h} ч {m} м",
        "tabs": ("  ИГРАТЬ  ", "  НАСТРОЙКИ  ", "  УПРАВЛЕНИЕ  "),
        "gdata": "ОБРАЗ ИГРЫ (.ISO / .CSO)",
        "sel": "ВЫБРАТЬ",
        "norom": "Файл игры не выбран (.iso / .cso)",
        "load": "Выбран: ",
        "mods": "МОДЫ:",
        "addm": "+ СТАВИТЬ МОД",
        "clrm": "СБРОС",
        "warn": "⚠ Внимание: моды и читы могут сломать игру. Ставьте стабильные PSP-моды.",
        "play": "▶  ЗАПУСТИТЬ ИГРУ",
        "run": "ИГРА ЗАПУЩЕНА...",
        "inp": "УПРАВЛЕНИЕ",
        "kb": "Клавиатура + Мышь (WASD + Клики мыши)",
        "gp": "Геймпад Xbox / PlayStation (XInput)",
        "res": "РАЗРЕШЕНИЕ ГРАФИКИ",
        "nat": "Родное",
        "perf": "ПРОИЗВОДИТЕЛЬНОСТЬ И ЭКРАН",
        "fps": "Разблокировать 60 FPS (Рекомендуется)",
        "low": "Режим для слабых ПК (Родное разрешение)",
        "fs": "Полноэкранный режим (16:9)",
        "vs": "Вертикальная синхронизация (VSync)",
        "sav": "СЕЙВЫ:",
        "bkp": "БЭКАП",
        "rsts": "ВОССТ.",
        "bkpok": "Сохранено в SaveStates_Backup.zip!",
        "rstok": "Сейв-стейты восстановлены!",
        "rstno": "Файл SaveStates_Backup.zip не найден.",
        "art": "ФОН:",
        "csta": "СВОЁ ФОТО",
        "rsta": "СБРОС",
        "modok": "Мод установлен: ",
        "clrask": "Удалить все моды и вернуть оригинал?",
        "clrok": "Все моды удалены!",
        "norom_w": "Сначала выберите образ игры (.iso / .cso)!",
        "keys": [
            ("W A S D", "Движение персонажа"),
            ("ПРОБЕЛ", "Прыжок / Двойной прыжок"),
            ("ЛКМ / J", "Лёгкая атака"),
            ("ПКМ / K", "Сильная атака"),
            ("SHIFT / L", "Блок / Захват / Действие"),
            ("1-4 / СТРЕЛКИ", "Выбор пришельца"),
            ("Q / E", "Омнитрикс / Камера"),
            ("F5 / F7", "Быстрый сейв / Загрузка"),
            ("ESC / TAB", "Пауза / Улучшения")
        ]
    },
    "de": {
        "sub": "REMASTERED PC  |  60 FPS BREITBILD",
        "time": "SPIELZEIT: {h}h {m}m",
        "tabs": ("  SPIELEN  ", "  EINSTELLUNGEN  ", "  STEUERUNG  "),
        "gdata": "SPIELDATEI (.ISO / .CSO)",
        "sel": "WÄHLEN",
        "norom": "Keine Spieldatei gewählt (.iso / .cso)",
        "load": "Geladen: ",
        "mods": "MODS:",
        "addm": "+ MOD INSTALLIEREN",
        "clrm": "LÖSCHEN",
        "warn": "⚠ Achtung: Mods/Cheats können das Spiel beschädigen (PSP-Version).",
        "play": "▶  SPIEL STARTEN",
        "run": "LÄUFT...",
        "inp": "STEUERUNG",
        "kb": "Tastatur + Maus (WASD + Mausklicks)",
        "gp": "Xbox / PlayStation Controller (XInput)",
        "res": "AUFLÖSUNG",
        "nat": "Nativ",
        "perf": "LEISTUNG & ANZEIGE",
        "fps": "60 FPS Modus freischalten (Empfohlen)",
        "low": "Schwacher PC Modus (Native Auflösung)",
        "fs": "Vollbildmodus (16:9 Breitbild)",
        "vs": "VSync aktivieren",
        "sav": "SAVES:",
        "bkp": "BACKUP",
        "rsts": "LADEN",
        "bkpok": "In SaveStates_Backup.zip gesichert!",
        "rstok": "Save States wiederhergestellt!",
        "rstno": "SaveStates_Backup.zip nicht gefunden.",
        "art": "BILD:",
        "csta": "FOTO",
        "rsta": "RESET",
        "modok": "Mod installiert: ",
        "clrask": "Alle Mods entfernen?",
        "clrok": "Alle Mods entfernt!",
        "norom_w": "Bitte zuerst Spieldatei (.iso / .cso) wählen!",
        "keys": [
            ("W A S D", "Bewegen"),
            ("LEERTASTE", "Springen / Doppelsprung"),
            ("LINKSKLICK / J", "Leichter Angriff"),
            ("RECHTSKLICK / K", "Starker Angriff"),
            ("SHIFT / L", "Blocken / Greifen"),
            ("1-4 / PFEILE", "Alien wählen"),
            ("Q / E", "Omnitrix / Kamera"),
            ("F5 / F7", "Schnellspeichern / Laden"),
            ("ESC / TAB", "Pause / Upgrades")
        ]
    },
    "ja": {
        "sub": "REMASTERED PC  |  60 FPS ワイド画面",
        "time": "プレイ時間: {h}時間 {m}分",
        "tabs": ("  プレイ  ", "  設定  ", "  操作方法  "),
        "gdata": "ゲームデータ (.ISO / .CSO)",
        "sel": "選択",
        "norom": "ゲーム未選択 (.iso / .cso)",
        "load": "選択済: ",
        "mods": "MOD:",
        "addm": "+ MOD導入",
        "clrm": "削除",
        "warn": "⚠ 注意: MODやチートはゲーム破損の原因になります（PSP版）。",
        "play": "▶  ゲーム開始",
        "run": "起動中...",
        "inp": "操作デバイス",
        "kb": "キーボード + マウス (WASD + クリック)",
        "gp": "Xbox / PlayStation コントローラー (XInput)",
        "res": "描画解像度",
        "nat": "標準",
        "perf": "パフォーマンス設定",
        "fps": "60 FPS モードを有効化 (推奨)",
        "low": "低スペックPCモード (標準解像度)",
        "fs": "フルスクリーン (16:9)",
        "vs": "垂直同期 (VSync)",
        "sav": "セーブ:",
        "bkp": "保存",
        "rsts": "復元",
        "bkpok": "SaveStates_Backup.zip に保存しました！",
        "rstok": "ステートセーブを復元しました！",
        "rstno": "バックアップが見つかりません。",
        "art": "背景:",
        "csta": "変更",
        "rsta": "戻す",
        "modok": "MOD導入完了: ",
        "clrask": "すべてのMODを削除しますか？",
        "clrok": "MODを削除しました！",
        "norom_w": "先にゲームファイル (.iso / .cso) を選択してください！",
        "keys": [
            ("W A S D", "移動"),
            ("SPACE", "ジャンプ / 二段ジャンプ"),
            ("左クリック / J", "弱攻撃"),
            ("右クリック / K", "強攻撃"),
            ("SHIFT / L", "ガード / つかむ"),
            ("1-4 / 矢印", "エイリアン選択"),
            ("Q / E", "オムニトリックス / カメラ"),
            ("F5 / F7", "クイックセーブ / ロード"),
            ("ESC / TAB", "ポーズ / 強化")
        ]
    }
}
class OmnitrixCanvas(tk.Canvas):
    def __init__(self, parent, size=56):
        super().__init__(parent, width=size, height=size, bg="#0D1117", highlightthickness=0)
        p = 5
        self.create_oval(p, p, size - p, size - p, fill="#161B22", outline="#39FF14", width=3)
        self.create_polygon(p + 10, p + 7, size - p - 10, p + 7, size // 2, size // 2, fill="#39FF14")
        self.create_polygon(p + 10, size - p - 7, size - p - 10, size - p - 7, size // 2, size // 2, fill="#39FF14")


class Ben10RemasteredApp:
    ART_W = 310
    ART_H = 484

    def __init__(self, root):
        self.root = root
        self.root.title("Ben 10: Protector of Earth — Remastered PC")
        self.root.configure(bg="#0D1117")
        icon_file = resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_file):
            try:
                self.root.iconbitmap(icon_file)
            except Exception:
                pass
        if sys.platform.startswith("win"):
            self.root.geometry("920x520")
            self.root.resizable(False, False)
        self.cfg = ConfigManager.load()
        if self.cfg.get("lang") not in LANGS:
            self.cfg["lang"] = "en"
        self.current_pil = None
        self.tk_photo = None
        self._fade_job = None
        self._proc = None
        self._start_ts = 0.0
        self._build_style()
        self._build_ui()
        self._apply_language(self.cfg["lang"])
        self._sync_low_pc_state()
        self._switch_art_for_tab(0, instant=True)

    def _tr(self, key):
        return LANGS[self.cfg.get("lang", "en")][key]

    def _playtime_str(self):
        sec = int(self.cfg.get("playtime_sec", 0))
        return self._tr("time").format(h=sec // 3600, m=(sec % 3600) // 60)

    def _build_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background="#0D1117", borderwidth=0)
        s.configure("TNotebook.Tab", background="#161B22", foreground="#C9D1D9", padding=(12, 6), font=("Arial", 9, "bold"))
        s.map("TNotebook.Tab", background=[("selected", "#21262D")], foreground=[("selected", "#39FF14")])
        s.configure("Dark.TFrame", background="#0D1117")
        s.configure("Card.TFrame", background="#161B22")
        s.configure("Dark.TRadiobutton", background="#161B22", foreground="#FFFFFF", font=("Arial", 9))
        s.configure("Dark.TCheckbutton", background="#161B22", foreground="#FFFFFF", font=("Arial", 9))

    def _build_ui(self):
        wrap = tk.Frame(self.root, bg="#0D1117")
        wrap.pack(fill="both", expand=True, padx=16, pady=16)
        left = tk.Frame(wrap, bg="#0D1117")
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        hdr = tk.Frame(left, bg="#0D1117", pady=2)
        hdr.pack(fill="x", pady=(0, 8))
        OmnitrixCanvas(hdr, 56).pack(side="left", padx=(0, 10))
        tf = tk.Frame(hdr, bg="#0D1117")
        tf.pack(side="left", fill="y", pady=1)
        tk.Label(tf, text="BEN 10: PROTECTOR OF EARTH", font=("Arial", 13, "bold"), bg="#0D1117", fg="#FFFFFF").pack(anchor="w")
        self.lbl_sub = tk.Label(tf, text="", font=("Arial", 7, "bold"), bg="#0D1117", fg="#39FF14")
        self.lbl_sub.pack(anchor="w")
        self.lbl_time = tk.Label(tf, text="", font=("Consolas", 8, "bold"), bg="#0D1117", fg="#8B949E")
        self.lbl_time.pack(anchor="w")
        lf = tk.Frame(hdr, bg="#0D1117")
        lf.pack(side="right", anchor="n")
        self.lang_btns = {}
        for code, lbl in [("en", "US"), ("ru", "RU"), ("de", "DE"), ("ja", "JP")]:
            b = tk.Button(lf, text=lbl, font=("Arial", 7, "bold"), bg="#161B22", fg="#8B949E", relief="flat", padx=5, pady=2, command=lambda c=code: self._set_lang(c))
            b.pack(side="left", padx=1)
            self.lang_btns[code] = b
        self.nb = ttk.Notebook(left)
        self.nb.pack(fill="both", expand=True)
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        t1, t2, t3 = ttk.Frame(self.nb, style="Dark.TFrame"), ttk.Frame(self.nb, style="Dark.TFrame"), ttk.Frame(self.nb, style="Dark.TFrame")
        self.nb.add(t1, text="PLAY")
        self.nb.add(t2, text="SETTINGS")
        self.nb.add(t3, text="CONTROLS")
        c1 = ttk.Frame(t1, style="Card.TFrame", padding=15)
        c1.pack(fill="both", expand=True, pady=(8, 0))
        self.lbl_gdata = tk.Label(c1, text="", font=("Arial", 9, "bold"), bg="#161B22", fg="#8B949E")
        self.lbl_gdata.pack(anchor="w")
        rf = tk.Frame(c1, bg="#0D1117", padx=10, pady=8)
        rf.pack(fill="x", pady=(6, 10))
        self.lbl_rom = tk.Label(rf, text="", font=("Arial", 9), bg="#0D1117", fg="#E6EDF3", wraplength=360, justify="left")
        self.lbl_rom.pack(side="left", fill="x", expand=True)
        self.btn_sel = tk.Button(rf, text="", font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=5, command=self._pick_rom)
        self.btn_sel.pack(side="right")
        mb = tk.Frame(c1, bg="#0D1117", padx=10, pady=8)
        mb.pack(fill="x", pady=(0, 8))
        self.lbl_mods = tk.Label(mb, text="", font=("Arial", 8, "bold"), bg="#0D1117", fg="#39FF14")
        self.lbl_mods.pack(side="left")
        self.btn_clrm = tk.Button(mb, text="", font=("Arial", 8, "bold"), bg="#21262D", fg="#F85149", relief="flat", padx=8, pady=4, command=self._clear_mods)
        self.btn_clrm.pack(side="right", padx=(6, 0))
        self.btn_addm = tk.Button(mb, text="", font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=4, command=self._install_mod)
        self.btn_addm.pack(side="right")
        self.lbl_warn = tk.Label(c1, text="", font=("Arial", 8), bg="#161B22", fg="#E3B341", justify="left", wraplength=520)
        self.lbl_warn.pack(anchor="w", pady=(0, 8))
        self.btn_play = tk.Button(c1, text="", font=("Arial", 13, "bold"), bg="#39FF14", fg="#0D1117", relief="flat", pady=11, command=self._play)
        self.btn_play.pack(side="bottom", fill="x")
        c2 = ttk.Frame(t2, style="Card.TFrame", padding=12)
        c2.pack(fill="both", expand=True, pady=(8, 0))
        self.lbl_inp = tk.Label(c2, text="", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
        self.lbl_inp.pack(anchor="w")
        self.v_ctrl = tk.StringVar(value=self.cfg["control_scheme"])
        self.rb_kb = ttk.Radiobutton(c2, text="", variable=self.v_ctrl, value="keyboard_mouse", style="Dark.TRadiobutton", command=self._save_opts)
        self.rb_kb.pack(anchor="w")
        self.rb_gp = ttk.Radiobutton(c2, text="", variable=self.v_ctrl, value="gamepad", style="Dark.TRadiobutton", command=self._save_opts)
        self.rb_gp.pack(anchor="w")
        self.lbl_res = tk.Label(c2, text="", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
        self.lbl_res.pack(anchor="w", pady=(6, 1))
        self.v_res = tk.StringVar(value=str(self.cfg["resolution"]))
        rf2 = tk.Frame(c2, bg="#161B22")
        rf2.pack(anchor="w")
        self.res_btns = []
        for txt, val in [("Native", "1"), ("720p", "2"), ("1080p", "3"), ("4K", "6")]:
            rb = ttk.Radiobutton(rf2, text=txt, variable=self.v_res, value=val, style="Dark.TRadiobutton", command=self._save_opts)
            rb.pack(side="left", padx=(0, 12))
            self.res_btns.append(rb)
        self.lbl_perf = tk.Label(c2, text="", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14")
        self.lbl_perf.pack(anchor="w", pady=(6, 1))
        self.v_fps60 = tk.BooleanVar(value=self.cfg.get("fps_60", True))
        self.v_lowpc = tk.BooleanVar(value=self.cfg.get("low_end_pc", False))
        self.v_fs = tk.BooleanVar(value=self.cfg.get("fullscreen", True))
        self.v_vs = tk.BooleanVar(value=self.cfg.get("vsync", False))
        self.cb_fps = ttk.Checkbutton(c2, text="", variable=self.v_fps60, style="Dark.TCheckbutton", command=self._save_opts)
        self.cb_fps.pack(anchor="w")
        self.cb_low = ttk.Checkbutton(c2, text="", variable=self.v_lowpc, style="Dark.TCheckbutton", command=self._on_low_pc_toggle)
        self.cb_low.pack(anchor="w")
        self.cb_fs = ttk.Checkbutton(c2, text="", variable=self.v_fs, style="Dark.TCheckbutton", command=self._save_opts)
        self.cb_fs.pack(anchor="w")
        self.cb_vs = ttk.Checkbutton(c2, text="", variable=self.v_vs, style="Dark.TCheckbutton", command=self._save_opts)
        self.cb_vs.pack(anchor="w")
        tb = tk.Frame(c2, bg="#0D1117", padx=8, pady=6)
        tb.pack(fill="x", side="bottom", pady=(4, 0))
        self.lbl_sav = tk.Label(tb, text="", font=("Arial", 7, "bold"), bg="#0D1117", fg="#39FF14")
        self.lbl_sav.pack(side="left")
        self.btn_bkp = tk.Button(tb, text="", font=("Arial", 7, "bold"), bg="#21262D", fg="#E6EDF3", relief="flat", padx=6, pady=2, command=self._backup_saves)
        self.btn_bkp.pack(side="left", padx=(4, 2))
        self.btn_rsts = tk.Button(tb, text="", font=("Arial", 7, "bold"), bg="#21262D", fg="#E6EDF3", relief="flat", padx=6, pady=2, command=self._restore_saves)
        self.btn_rsts.pack(side="left", padx=2)
        self.btn_rsta = tk.Button(tb, text="", font=("Arial", 7, "bold"), bg="#21262D", fg="#C9D1D9", relief="flat", padx=6, pady=2, command=self._reset_custom_art)
        self.btn_rsta.pack(side="right", padx=(2, 0))
        self.btn_csta = tk.Button(tb, text="", font=("Arial", 7, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=6, pady=2, command=self._pick_custom_art)
        self.btn_csta.pack(side="right", padx=2)
        self.lbl_art = tk.Label(tb, text="", font=("Arial", 7, "bold"), bg="#0D1117", fg="#8B949E")
        self.lbl_art.pack(side="right")
        self.c3 = ttk.Frame(t3, style="Card.TFrame", padding=14)
        self.c3.pack(fill="both", expand=True, pady=(8, 0))
        rf_art = tk.Frame(wrap, bg="#39FF14", padx=2, pady=2)
        rf_art.pack(side="right", fill="y")
                self.art_canvas = tk.Canvas(rf_art, width=self.ART_W, height=self.ART_H, bg="#161B22", highlightthickness=0)
        self.art_canvas.pack()

    def _set_lang(self, code):
        self.cfg["lang"] = code
        ConfigManager.save(self.cfg)
        self._apply_language(code)

    def _apply_language(self, code):
        for c, b in self.lang_btns.items():
            b.configure(bg="#39FF14" if c == code else "#161B22", fg="#0D1117" if c == code else "#8B949E")
        self.lbl_sub.config(text=self._tr("sub"))
        self.lbl_time.config(text=self._playtime_str())
        for i, t in enumerate(self._tr("tabs")):
            self.nb.tab(i, text=t)
        self.lbl_gdata.config(text=self._tr("gdata"))
        self.btn_sel.config(text=self._tr("sel"))
        self.lbl_rom.config(text=self._rom_txt())
        self.lbl_mods.config(text=self._tr("mods"))
        self.btn_addm.config(text=self._tr("addm"))
        self.btn_clrm.config(text=self._tr("clrm"))
        self.lbl_warn.config(text=self._tr("warn"))
        self.btn_play.config(text=self._tr("play"))
        self.lbl_inp.config(text=self._tr("inp"))
        self.rb_kb.config(text=self._tr("kb"))
        self.rb_gp.config(text=self._tr("gp"))
        self.lbl_res.config(text=self._tr("res"))
        self.res_btns[0].config(text=self._tr("nat"))
        self.lbl_perf.config(text=self._tr("perf"))
        self.cb_fps.config(text=self._tr("fps"))
        self.cb_low.config(text=self._tr("low"))
        self.cb_fs.config(text=self._tr("fs"))
        self.cb_vs.config(text=self._tr("vs"))
        self.lbl_sav.config(text=self._tr("sav"))
        self.btn_bkp.config(text=self._tr("bkp"))
        self.btn_rsts.config(text=self._tr("rsts"))
        self.lbl_art.config(text=self._tr("art"))
        self.btn_csta.config(text=self._tr("csta"))
        self.btn_rsta.config(text=self._tr("rsta"))
        for w in self.c3.winfo_children():
            w.destroy()
        for k, desc in self._tr("keys"):
            row = tk.Frame(self.c3, bg="#161B22")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=("Consolas", 8, "bold"), bg="#0D1117", fg="#39FF14", width=18).pack(side="left", padx=(0, 10))
            tk.Label(row, text=desc, font=("Arial", 8), bg="#161B22", fg="#C9D1D9").pack(side="left")

    def _backup_saves(self):
        try:
            ConfigManager.backup_saves()
            messagebox.showinfo("OK", self._tr("bkpok"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _restore_saves(self):
        try:
            if ConfigManager.restore_saves():
                messagebox.showinfo("OK", self._tr("rstok"))
            else:
                messagebox.showwarning("Warning", self._tr("rstno"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _install_mod(self):
        p = filedialog.askopenfilename(filetypes=[("Any Mod File", "*.*"), ("Archives & Cheats", "*.zip *.ini")])
        if p:
            try:
                name = ConfigManager.install_any_mod(p)
                messagebox.showinfo("OK", f"{self._tr('modok')}{name}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _clear_mods(self):
        if messagebox.askyesno("Reset", self._tr("clrask")):
            ConfigManager.clear_all_mods()
            messagebox.showinfo("OK", self._tr("clrok"))

    def _load_pil_art(self, path):
        if not HAS_PIL or not path or not os.path.exists(path):
            return None
        try:
            return Image.open(path).convert("RGB").resize((self.ART_W, self.ART_H), Image.Resampling.LANCZOS)
        except Exception:
            return None

    def _switch_art_for_tab(self, tab_idx, instant=False):
        custom = self.cfg.get("custom_art", "")
        target_path = custom if (custom and os.path.exists(custom)) else resource_path(os.path.join("assets", "art_play.png" if tab_idx == 0 else "art_settings.png"))
        target_img = self._load_pil_art(target_path)
        if target_img is None:
            self.art_canvas.delete("all")
            self.art_canvas.create_text(self.ART_W // 2, self.ART_H // 2, text="BEN 10\nREMASTERED PC", fill="#39FF14", font=("Arial", 14, "bold"), justify="center")
            return
        if self._fade_job:
            self.root.after_cancel(self._fade_job)
            self._fade_job = None
        if instant or self.current_pil is None:
            self.current_pil = target_img
            self.tk_photo = ImageTk.PhotoImage(target_img)
            self.art_canvas.delete("all")
            self.art_canvas.create_image(0, 0, anchor="nw", image=self.tk_photo)
        else:
            self._animate_fade(self.current_pil, target_img, 1, 8)

    def _animate_fade(self, img1, img2, step, total):
        blended = Image.blend(img1, img2, step / float(total))
        self.tk_photo = ImageTk.PhotoImage(blended)
        self.art_canvas.delete("all")
        self.art_canvas.create_image(0, 0, anchor="nw", image=self.tk_photo)
        if step < total:
            self._fade_job = self.root.after(28, lambda: self._animate_fade(img1, img2, step + 1, total))
        else:
            self.current_pil = img2
            self._fade_job = None

    def _on_tab_changed(self, _e):
        self._switch_art_for_tab(self.nb.index(self.nb.select()), instant=False)

    def _pick_custom_art(self):
        p = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp"), ("All", "*.*")])
        if p:
            self.cfg["custom_art"] = p
            ConfigManager.save(self.cfg)
            self._switch_art_for_tab(self.nb.index(self.nb.select()), instant=False)

    def _reset_custom_art(self):
        self.cfg["custom_art"] = ""
        ConfigManager.save(self.cfg)
        self._switch_art_for_tab(self.nb.index(self.nb.select()), instant=False)

    def _sync_low_pc_state(self):
        is_low = self.v_lowpc.get()
        for rb in self.res_btns:
            rb.configure(state="disabled" if is_low else "normal")
        if is_low:
            self.v_res.set("1")

    def _on_low_pc_toggle(self):
        self._sync_low_pc_state()
        self._save_opts()

    def _rom_txt(self):
        p = self.cfg.get("game_path", "")
        return f"{self._tr('load')}{os.path.basename(p)}" if (p and os.path.exists(p)) else self._tr("norom")

    def _pick_rom(self):
        p = filedialog.askopenfilename(filetypes=[("PSP Game Data", "*.iso *.cso"), ("All", "*.*")])
        if p:
            self.cfg["game_path"] = p
            ConfigManager.save(self.cfg)
            self.lbl_rom.config(text=self._rom_txt())

    def _save_opts(self):
        self.cfg.update({"control_scheme": self.v_ctrl.get(), "resolution": self.v_res.get(), "fullscreen": self.v_fs.get(), "vsync": self.v_vs.get(), "fps_60": self.v_fps60.get(), "low_end_pc": self.v_lowpc.get()})
        ConfigManager.save(self.cfg)

    def _watch_game_process(self):
        if self._proc is None:
            return
        if self._proc.poll() is None:
            self.root.after(1000, self._watch_game_process)
            return
        self.cfg["playtime_sec"] = int(self.cfg.get("playtime_sec", 0)) + max(0, int(time.time() - self._start_ts))
        ConfigManager.save(self.cfg)
        self._proc = None
        self.root.deiconify()
        self.lbl_time.config(text=self._playtime_str())
        self.btn_play.configure(state="normal", text=self._tr("play"))

    def _play(self):
        gp = self.cfg.get("game_path", "")
        if not gp or not os.path.exists(gp):
            messagebox.showwarning("Warning", self._tr("norom_w"))
            return
        self.btn_play.configure(state="disabled", text=self._tr("run"))
        self.root.update_idletasks()
        try:
            ConfigManager.apply_settings(self.cfg)
            exe = os.path.join(BASE_DIR, "Engine", "Ben10Game.exe")
            if not sys.platform.startswith("win"):
                messagebox.showinfo("OK", "Config ready!")
                self.btn_play.configure(state="normal", text=self._tr("play"))
                return
            if not os.path.exists(exe):
                messagebox.showerror("Error", "Engine/Ben10Game.exe not found.")
                self.btn_play.configure(state="normal", text=self._tr("play"))
                return
            self._start_ts = time.time()
            self._proc = subprocess.Popen([exe, "--fullscreen", gp])
            self.root.withdraw()
            self.root.after(1000, self._watch_game_process)
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", str(e))
            self.btn_play.configure(state="normal", text=self._tr("play"))


if __name__ == "__main__":
    root = tk.Tk()
    Ben10RemasteredApp(root)
    root.mainloop()
                    self.cfg["playtime_sec"] = int(self.cfg.get("playtime_sec", 0)) + max(0, int(time.time() - self._start_ts))
        ConfigManager.save(self.cfg)
        self._proc = None
        self.root.deiconify()
        self.lbl_time.config(text=self._playtime_str())
        self.btn_play.configure(state="normal", text=self._tr("play"))

    def _play(self):
        gp = self.cfg.get("game_path", "")
        if not gp or not os.path.exists(gp):
            messagebox.showwarning("Warning", self._tr("norom_w"))
            return
        self.btn_play.configure(state="disabled", text=self._tr("run"))
        self.root.update_idletasks()
        try:
            ConfigManager.apply_settings(self.cfg)
            exe = os.path.join(BASE_DIR, "Engine", "Ben10Game.exe")
            if not sys.platform.startswith("win"):
                messagebox.showinfo("OK", "Config ready!")
                self.btn_play.configure(state="normal", text=self._tr("play"))
                return
            if not os.path.exists(exe):
                messagebox.showerror("Error", "Engine/Ben10Game.exe not found.")
                self.btn_play.configure(state="normal", text=self._tr("play"))
                return
            self._start_ts = time.time()
            self._proc = subprocess.Popen([exe, "--fullscreen", gp])
            self.root.withdraw()
            self.root.after(1000, self._watch_game_process)
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", str(e))
            self.btn_play.configure(state="normal", text=self._tr("play"))


if __name__ == "__main__":
    root = tk.Tk()
    Ben10RemasteredApp(root)
    root.mainloop()
