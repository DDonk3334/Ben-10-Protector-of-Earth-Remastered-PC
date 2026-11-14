import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, subprocess, sys, time
from backend import BASE_DIR, ConfigManager

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def resource_path(rel):
    return os.path.join(getattr(sys, "_MEIPASS", BASE_DIR), rel)

LANGS = {
    "en": ("REMASTERED PC | 60 FPS", "PLAYTIME: {h}h {m}m", (" PLAY ", " SETTINGS ", " CONTROLS "), "GAME FILE (.ISO/.CSO)", "SELECT", "No file selected", "Loaded: ", "MODS:", "+ MOD", "CLEAR", "⚠ Mods/cheats may break the game. Use stable PSP mods.", "▶ PLAY GAME", "RUNNING...", "INPUT", "Keyboard + Mouse (WASD + Clicks)", "Gamepad (XInput)", "RESOLUTION", "Native", "PERFORMANCE", "Unlock 60 FPS", "Low-End PC Mode", "Fullscreen (16:9)", "VSync", "SAVES:", "BACKUP", "RESTORE", "Saved to SaveStates_Backup.zip!", "Saves restored!", "No backup found.", "ART:", "CUSTOM", "RESET", "Installed: ", "Remove all mods?", "Mods cleared!", "Select game file first!", [("WASD", "Move"), ("SPACE", "Jump"), ("LMB / J", "Light Attack"), ("RMB / K", "Heavy Attack"), ("SHIFT / L", "Block / Grab"), ("1-4 / ARROWS", "Select Alien"), ("Q / E", "Omnitrix / Cam"), ("F5 / F7", "Quick Save / Load"), ("ESC / TAB", "Pause / Upgrades")]),
    "ru": ("REMASTERED PC | 60 FPS", "В ИГРЕ: {h} ч {m} м", (" ИГРАТЬ ", " НАСТРОЙКИ ", " УПРАВЛЕНИЕ "), "ОБРАЗ ИГРЫ (.ISO/.CSO)", "ВЫБРАТЬ", "Файл не выбран", "Выбран: ", "МОДЫ:", "+ МОД", "СБРОС", "⚠ Моды и читы могут сломать игру. Ставьте стабильные PSP-моды.", "▶ ЗАПУСТИТЬ", "ЗАПУЩЕНА...", "УПРАВЛЕНИЕ", "Клавиатура + Мышь (WASD + Клики)", "Геймпад (XInput)", "РАЗРЕШЕНИЕ", "Родное", "ПРОИЗВОДИТЕЛЬНОСТЬ", "Разблокировать 60 FPS", "Режим для слабых ПК", "Полный экран (16:9)", "VSync", "СЕЙВЫ:", "БЭКАП", "ВОССТ.", "Сохранено в SaveStates_Backup.zip!", "Сейвы восстановлены!", "Бэкап не найден.", "ФОН:", "СВОЁ", "СБРОС", "Установлен: ", "Удалить все моды?", "Моды удалены!", "Сначала выберите образ игры!", [("WASD", "Движение"), ("ПРОБЕЛ", "Прыжок"), ("ЛКМ / J", "Лёгкая атака"), ("ПКМ / K", "Сильная атака"), ("SHIFT / L", "Блок / Захват"), ("1-4 / СТРЕЛКИ", "Выбор пришельца"), ("Q / E", "Омнитрикс / Камера"), ("F5 / F7", "Сейв / Загрузка"), ("ESC / TAB", "Пауза / Улучшения")]),
    "de": ("REMASTERED PC | 60 FPS", "SPIELZEIT: {h}h {m}m", (" SPIELEN ", " OPTIONEN ", " STEUERUNG "), "SPIELDATEI (.ISO/.CSO)", "WÄHLEN", "Keine Datei gewählt", "Geladen: ", "MODS:", "+ MOD", "LÖSCHEN", "⚠ Mods/Cheats können das Spiel beschädigen (PSP-Version).", "▶ STARTEN", "LÄUFT...", "EINGABE", "Tastatur + Maus (WASD + Klicks)", "Gamepad (XInput)", "AUFLÖSUNG", "Nativ", "LEISTUNG", "60 FPS freischalten", "Schwacher PC Modus", "Vollbild (16:9)", "VSync", "SAVES:", "BACKUP", "LADEN", "In SaveStates_Backup.zip gesichert!", "Wiederhergestellt!", "Kein Backup gefunden.", "BILD:", "FOTO", "RESET", "Installiert: ", "Alle Mods löschen?", "Mods gelöscht!", "Bitte Spieldatei wählen!", [("WASD", "Bewegen"), ("SPACE", "Springen"), ("LMB / J", "Leichter Angriff"), ("RMB / K", "Starker Angriff"), ("SHIFT / L", "Blocken / Greifen"), ("1-4 / PFEILE", "Alien wählen"), ("Q / E", "Omnitrix / Kamera"), ("F5 / F7", "Speichern / Laden"), ("ESC / TAB", "Pause / Upgrades")]),
    "ja": ("REMASTERED PC | 60 FPS", "プレイ時間: {h}時間 {m}分", (" プレイ ", " 設定 ", " 操作 "), "ゲームデータ (.ISO/.CSO)", "選択", "ファイル未選択", "選択済: ", "MOD:", "+ MOD", "削除", "⚠ MODやチートはゲーム破損の原因になります（PSP版）。", "▶ ゲーム開始", "起動中...", "操作", "キーボード + マウス (WASD)", "コントローラー (XInput)", "解像度", "標準", "設定", "60 FPS 有効化", "低スペックPCモード", "フルスクリーン (16:9)", "VSync", "セーブ:", "保存", "復元", "SaveStates_Backup.zip に保存完了！", "復元しました！", "バックアップなし", "背景:", "変更", "戻す", "導入完了: ", "MODを削除しますか？", "削除完了！", "ゲームファイルを選択してください！", [("WASD", "移動"), ("SPACE", "ジャンプ"), ("LMB / J", "弱攻撃"), ("RMB / K", "強攻撃"), ("SHIFT / L", "ガード / つかむ"), ("1-4 / 矢印", "エイリアン選択"), ("Q / E", "オムニトリックス"), ("F5 / F7", "セーブ / ロード"), ("ESC / TAB", "ポーズ / 強化")])
}

class OmnitrixCanvas(tk.Canvas):
    def __init__(self, p, s=56):
        super().__init__(p, width=s, height=s, bg="#0D1117", highlightthickness=0)
        self.create_oval(5, 5, s-5, s-5, fill="#161B22", outline="#39FF14", width=3)
        self.create_polygon(15, 12, s-15, 12, s//2, s//2, fill="#39FF14")
        self.create_polygon(15, s-12, s-15, s-12, s//2, s//2, fill="#39FF14")

class Ben10RemasteredApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ben 10: Protector of Earth — Remastered PC")
        self.root.configure(bg="#0D1117")
        ico = resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(ico):
            try: self.root.iconbitmap(ico)
            except Exception: pass
        if sys.platform.startswith("win"):
            self.root.geometry("920x520")
            self.root.resizable(False, False)
        self.cfg = ConfigManager.load()
        if self.cfg.get("lang") not in LANGS: self.cfg["lang"] = "en"
        self.cur_pil = self.tk_img = self._fjob = self._proc = None
        self._t0 = 0.0
        self._style()
        self._ui()
        self._apply_lang(self.cfg["lang"])
        self._sync_low()
        self._set_art(0, True)

    def _t(self, i): return LANGS[self.cfg.get("lang", "en")][i]

    def _style(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("TNotebook", background="#0D1117", borderwidth=0)
        s.configure("TNotebook.Tab", background="#161B22", foreground="#C9D1D9", padding=(12, 6), font=("Arial", 9, "bold"))
        s.map("TNotebook.Tab", background=[("selected", "#21262D")], foreground=[("selected", "#39FF14")])
        for n, bg in [("Dark.TFrame", "#0D1117"), ("Card.TFrame", "#161B22")]: s.configure(n, background=bg)
        for n in ["Dark.TRadiobutton", "Dark.TCheckbutton"]: s.configure(n, background="#161B22", foreground="#FFF", font=("Arial", 9))
    def _ui(self):
        w = tk.Frame(self.root, bg="#0D1117"); w.pack(fill="both", expand=True, padx=16, pady=16)
        l = tk.Frame(w, bg="#0D1117"); l.pack(side="left", fill="both", expand=True, padx=(0, 14))
        h = tk.Frame(l, bg="#0D1117"); h.pack(fill="x", pady=(0, 8))
        OmnitrixCanvas(h).pack(side="left", padx=(0, 10))
        tf = tk.Frame(h, bg="#0D1117"); tf.pack(side="left")
        tk.Label(tf, text="BEN 10: PROTECTOR OF EARTH", font=("Arial", 13, "bold"), bg="#0D1117", fg="#FFF").pack(anchor="w")
        self.l_sub = tk.Label(tf, font=("Arial", 7, "bold"), bg="#0D1117", fg="#39FF14"); self.l_sub.pack(anchor="w")
        self.l_tm = tk.Label(tf, font=("Consolas", 8, "bold"), bg="#0D1117", fg="#8B949E"); self.l_tm.pack(anchor="w")
        lf = tk.Frame(h, bg="#0D1117"); lf.pack(side="right", anchor="n")
        self.lbtns = {c: tk.Button(lf, text=lbl, font=("Arial", 7, "bold"), relief="flat", padx=5, pady=2, command=lambda x=c: self._lang(x)) for c, lbl in [("en","US"),("ru","RU"),("de","DE"),("ja","JP")]}
        for b in self.lbtns.values(): b.pack(side="left", padx=1)

        self.nb = ttk.Notebook(l); self.nb.pack(fill="both", expand=True)
        self.nb.bind("<<NotebookTabChanged>>", lambda e: self._set_art(self.nb.index(self.nb.select())))
        t1, t2, t3 = ttk.Frame(self.nb, style="Dark.TFrame"), ttk.Frame(self.nb, style="Dark.TFrame"), ttk.Frame(self.nb, style="Dark.TFrame")
        for t in (t1, t2, t3): self.nb.add(t, text=" ")

        c1 = ttk.Frame(t1, style="Card.TFrame", padding=15); c1.pack(fill="both", expand=True, pady=(8, 0))
        self.l_gd = tk.Label(c1, font=("Arial", 9, "bold"), bg="#161B22", fg="#8B949E"); self.l_gd.pack(anchor="w")
        rf = tk.Frame(c1, bg="#0D1117", padx=10, pady=8); rf.pack(fill="x", pady=(6, 10))
        self.l_rom = tk.Label(rf, font=("Arial", 9), bg="#0D1117", fg="#E6EDF3", wraplength=360, justify="left"); self.l_rom.pack(side="left", fill="x", expand=True)
        self.b_sel = tk.Button(rf, font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=5, command=self._pick_rom); self.b_sel.pack(side="right")
        mb = tk.Frame(c1, bg="#0D1117", padx=10, pady=8); mb.pack(fill="x", pady=(0, 8))
        self.l_mod = tk.Label(mb, font=("Arial", 8, "bold"), bg="#0D1117", fg="#39FF14"); self.l_mod.pack(side="left")
        self.b_clrm = tk.Button(mb, font=("Arial", 8, "bold"), bg="#21262D", fg="#F85149", relief="flat", padx=8, pady=4, command=self._clr_mod); self.b_clrm.pack(side="right", padx=(6, 0))
        self.b_addm = tk.Button(mb, font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=4, command=self._add_mod); self.b_addm.pack(side="right")
        self.l_wrn = tk.Label(c1, font=("Arial", 8), bg="#161B22", fg="#E3B341", justify="left", wraplength=520); self.l_wrn.pack(anchor="w", pady=(0, 8))
        self.b_play = tk.Button(c1, font=("Arial", 13, "bold"), bg="#39FF14", fg="#0D1117", relief="flat", pady=11, command=self._play); self.b_play.pack(side="bottom", fill="x")

        c2 = ttk.Frame(t2, style="Card.TFrame", padding=12); c2.pack(fill="both", expand=True, pady=(8, 0))
        self.l_inp = tk.Label(c2, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14"); self.l_inp.pack(anchor="w")
        self.v_ctrl = tk.StringVar(value=self.cfg["control_scheme"])
        self.r_kb = ttk.Radiobutton(c2, variable=self.v_ctrl, value="keyboard_mouse", style="Dark.TRadiobutton", command=self._save); self.r_kb.pack(anchor="w")
        self.r_gp = ttk.Radiobutton(c2, variable=self.v_ctrl, value="gamepad", style="Dark.TRadiobutton", command=self._save); self.r_gp.pack(anchor="w")
        self.l_res = tk.Label(c2, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14"); self.l_res.pack(anchor="w", pady=(6, 1))
        self.v_res = tk.StringVar(value=str(self.cfg["resolution"]))
        rf2 = tk.Frame(c2, bg="#161B22"); rf2.pack(anchor="w")
        self.rbtns = [ttk.Radiobutton(rf2, text=tx, variable=self.v_res, value=vl, style="Dark.TRadiobutton", command=self._save) for tx, vl in [("Native","1"),("720p","2"),("1080p","3"),("4K","6")]]
        for rb in self.rbtns: rb.pack(side="left", padx=(0, 12))
        self.l_prf = tk.Label(c2, font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14"); self.l_prf.pack(anchor="w", pady=(6, 1))
        self.v_fps, self.v_low, self.v_fs, self.v_vs = tk.BooleanVar(value=self.cfg.get("fps_60", True)), tk.BooleanVar(value=self.cfg.get("low_end_pc", False)), tk.BooleanVar(value=self.cfg.get("fullscreen", True)), tk.BooleanVar(value=self.cfg.get("vsync", False))
        self.c_fps = ttk.Checkbutton(c2, variable=self.v_fps, style="Dark.TCheckbutton", command=self._save); self.c_fps.pack(anchor="w")
        self.c_low = ttk.Checkbutton(c2, variable=self.v_low, style="Dark.TCheckbutton", command=self._tgl_low); self.c_low.pack(anchor="w")
        self.c_fs = ttk.Checkbutton(c2, variable=self.v_fs, style="Dark.TCheckbutton", command=self._save); self.c_fs.pack(anchor="w")
        self.c_vs = ttk.Checkbutton(c2, variable=self.v_vs, style="Dark.TCheckbutton", command=self._save); self.c_vs.pack(anchor="w")

        tb = tk.Frame(c2, bg="#0D1117", padx=8, pady=6); tb.pack(fill="x", side="bottom", pady=(4, 0))
        self.l_sav = tk.Label(tb, font=("Arial", 7, "bold"), bg="#0D1117", fg="#39FF14"); self.l_sav.pack(side="left")
        self.b_bkp = tk.Button(tb, font=("Arial", 7, "bold"), bg="#21262D", fg="#E6EDF3", relief="flat", padx=6, pady=2, command=self._bkp); self.b_bkp.pack(side="left", padx=4)
        self.b_rsts = tk.Button(tb, font=("Arial", 7, "bold"), bg="#21262D", fg="#E6EDF3", relief="flat", padx=6, pady=2, command=self._rsts); self.b_rsts.pack(side="left")
        self.b_rsta = tk.Button(tb, font=("Arial", 7, "bold"), bg="#21262D", fg="#C9D1D9", relief="flat", padx=6, pady=2, command=self._rsta); self.b_rsta.pack(side="right", padx=(2, 0))
        self.b_csta = tk.Button(tb, font=("Arial", 7, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=6, pady=2, command=self._csta); self.b_csta.pack(side="right", padx=2)
        self.l_art = tk.Label(tb, font=("Arial", 7, "bold"), bg="#0D1117", fg="#8B949E"); self.l_art.pack(side="right")

        self.c3 = ttk.Frame(t3, style="Card.TFrame", padding=14); self.c3.pack(fill="both", expand=True, pady=(8, 0))
        af = tk.Frame(w, bg="#39FF14", padx=2, pady=2); af.pack(side="right", fill="y")
        self.cv = tk.Canvas(af, width=310, height=484, bg="#161B22", highlightthickness=0); self.cv.pack()
            def _lang(self, c):
        self.cfg["lang"] = c; ConfigManager.save(self.cfg); self._apply_lang(c)

    def _apply_lang(self, c):
        for k, b in self.lbtns.items(): b.configure(bg="#39FF14" if k == c else "#161B22", fg="#0D1117" if k == c else "#8B949E")
        sec = int(self.cfg.get("playtime_sec", 0))
        self.l_sub.config(text=self._t(0)); self.l_tm.config(text=self._t(1).format(h=sec//3600, m=(sec%3600)//60))
        for i, tx in enumerate(self._t(2)): self.nb.tab(i, text=tx)
        self.l_gd.config(text=self._t(3)); self.b_sel.config(text=self._t(4))
        p = self.cfg.get("game_path", "")
        self.l_rom.config(text=f"{self._t(6)}{os.path.basename(p)}" if p and os.path.exists(p) else self._t(5))
        self.l_mod.config(text=self._t(7)); self.b_addm.config(text=self._t(8)); self.b_clrm.config(text=self._t(9)); self.l_wrn.config(text=self._t(10)); self.b_play.config(text=self._t(11))
        self.l_inp.config(text=self._t(13)); self.r_kb.config(text=self._t(14)); self.r_gp.config(text=self._t(15))
        self.l_res.config(text=self._t(16)); self.rbtns[0].config(text=self._t(17)); self.l_prf.config(text=self._t(18))
        self.c_fps.config(text=self._t(19)); self.c_low.config(text=self._t(20)); self.c_fs.config(text=self._t(21)); self.c_vs.config(text=self._t(22))
        self.l_sav.config(text=self._t(23)); self.b_bkp.config(text=self._t(24)); self.b_rsts.config(text=self._t(25))
        self.l_art.config(text=self._t(29)); self.b_csta.config(text=self._t(30)); self.b_rsta.config(text=self._t(31))
        for ch in self.c3.winfo_children(): ch.destroy()
        for k, d in self._t(36):
            r = tk.Frame(self.c3, bg="#161B22"); r.pack(fill="x", pady=2)
            tk.Label(r, text=k, font=("Consolas", 8, "bold"), bg="#0D1117", fg="#39FF14", width=16).pack(side="left", padx=(0, 10))
            tk.Label(r, text=d, font=("Arial", 8), bg="#161B22", fg="#C9D1D9").pack(side="left")

    def _bkp(self):
        try: ConfigManager.backup_saves(); messagebox.showinfo("OK", self._t(26))
        except Exception as e: messagebox.showerror("Error", str(e))

    def _rsts(self):
        try: messagebox.showinfo("OK", self._t(27)) if ConfigManager.restore_saves() else messagebox.showwarning("Warning", self._t(28))
        except Exception as e: messagebox.showerror("Error", str(e))

    def _add_mod(self):
        p = filedialog.askopenfilename(filetypes=[("Mod", "*.*")])
        if p:
            try: messagebox.showinfo("OK", f"{self._t(32)}{ConfigManager.install_any_mod(p)}")
            except Exception as e: messagebox.showerror("Error", str(e))

    def _clr_mod(self):
        if messagebox.askyesno("Reset", self._t(33)): ConfigManager.clear_all_mods(); messagebox.showinfo("OK", self._t(34))

    def _set_art(self, idx, inst=False):
        c = self.cfg.get("custom_art", "")
        pt = c if (c and os.path.exists(c)) else resource_path(os.path.join("assets", "art_play.png" if idx == 0 else "art_settings.png"))
        im = Image.open(pt).convert("RGB").resize((310, 484), Image.Resampling.LANCZOS) if (HAS_PIL and pt and os.path.exists(pt)) else None
        if not im:
            self.cv.delete("all"); self.cv.create_text(155, 242, text="BEN 10\nREMASTERED PC", fill="#39FF14", font=("Arial", 14, "bold"), justify="center"); return
        if self._fjob: self.root.after_cancel(self._fjob); self._fjob = None
        if inst or not self.cur_pil:
            self.cur_pil = im; self.tk_img = ImageTk.PhotoImage(im); self.cv.delete("all"); self.cv.create_image(0, 0, anchor="nw", image=self.tk_img)
        else: self._fade(self.cur_pil, im, 1)

    def _fade(self, i1, i2, st):
        self.tk_img = ImageTk.PhotoImage(Image.blend(i1, i2, st / 8.0))
        self.cv.delete("all"); self.cv.create_image(0, 0, anchor="nw", image=self.tk_img)
        if st < 8: self._fjob = self.root.after(28, lambda: self._fade(i1, i2, st + 1))
        else: self.cur_pil = i2; self._fjob = None

    def _csta(self):
        p = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg *.webp")])
        if p: self.cfg["custom_art"] = p; ConfigManager.save(self.cfg); self._set_art(self.nb.index(self.nb.select()))

    def _rsta(self):
        self.cfg["custom_art"] = ""; ConfigManager.save(self.cfg); self._set_art(self.nb.index(self.nb.select()))

    def _sync_low(self):
        low = self.v_low.get()
        for rb in self.rbtns: rb.configure(state="disabled" if low else "normal")
        if low: self.v_res.set("1")

    def _tgl_low(self): self._sync_low(); self._save()

    def _pick_rom(self):
        p = filedialog.askopenfilename(filetypes=[("PSP Game", "*.iso *.cso"), ("All", "*.*")])
        if p: self.cfg["game_path"] = p; ConfigManager.save(self.cfg); self.l_rom.config(text=f"{self._t(6)}{os.path.basename(p)}")

    def _save(self):
        self.cfg.update({"control_scheme": self.v_ctrl.get(), "resolution": self.v_res.get(), "fullscreen": self.v_fs.get(), "vsync": self.v_vs.get(), "fps_60": self.v_fps.get(), "low_end_pc": self.v_low.get()})
        ConfigManager.save(self.cfg)

    def _watch(self):
        if not self._proc: return
        if self._proc.poll() is None: self.root.after(1000, self._watch); return
        self.cfg["playtime_sec"] = int(self.cfg.get("playtime_sec", 0)) + max(0, int(time.time() - self._t0))
        ConfigManager.save(self.cfg); self._proc = None; self.root.deiconify(); self._apply_lang(self.cfg["lang"]); self.b_play.configure(state="normal", text=self._t(11))

    def _play(self):
        gp = self.cfg.get("game_path", "")
        if not gp or not os.path.exists(gp): messagebox.showwarning("Warning", self._t(35)); return
        self.b_play.configure(state="disabled", text=self._t(12)); self.root.update_idletasks()
        try:
            ConfigManager.apply_settings(self.cfg)
            exe = os.path.join(BASE_DIR, "Engine", "Ben10Game.exe")
            if not sys.platform.startswith("win"): messagebox.showinfo("OK", "Ready!"); self.b_play.configure(state="normal", text=self._t(11)); return
            if not os.path.exists(exe): messagebox.showerror("Error", "Engine/Ben10Game.exe not found."); self.b_play.configure(state="normal", text=self._t(11)); return
            self._t0 = time.time(); self._proc = subprocess.Popen([exe, "--fullscreen", gp]); self.root.withdraw(); self.root.after(1000, self._watch)
        except Exception as e:
            self.root.deiconify(); messagebox.showerror("Error", str(e)); self.b_play.configure(state="normal", text=self._t(11))

if __name__ == "__main__":
    r = tk.Tk(); Ben10RemasteredApp(r); r.mainloop()
            
