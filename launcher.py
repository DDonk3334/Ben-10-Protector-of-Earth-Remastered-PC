import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import sys
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


class OmnitrixCanvas(tk.Canvas):
    def __init__(self, parent, size=62):
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
        self.current_pil = None
        self.tk_photo = None
        self._fade_job = None

        self._build_style()
        self._build_ui()
        self._sync_low_pc_state()
        self._switch_art_for_tab(0, instant=True)

    def _build_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background="#0D1117", borderwidth=0)
        s.configure("TNotebook.Tab", background="#161B22", foreground="#C9D1D9", padding=(14, 6), font=("Arial", 9, "bold"))
        s.map("TNotebook.Tab", background=[("selected", "#21262D")], foreground=[("selected", "#39FF14")])
        s.configure("Dark.TFrame", background="#0D1117")
        s.configure("Card.TFrame", background="#161B22")
        s.configure("Dark.TRadiobutton", background="#161B22", foreground="#FFFFFF", font=("Arial", 9))
        s.configure("Dark.TCheckbutton", background="#161B22", foreground="#FFFFFF", font=("Arial", 9))

    def _build_ui(self):
        main_wrap = tk.Frame(self.root, bg="#0D1117")
        main_wrap.pack(fill="both", expand=True, padx=16, pady=16)

        left_col = tk.Frame(main_wrap, bg="#0D1117")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 14))

        hdr = tk.Frame(left_col, bg="#0D1117", pady=4)
        hdr.pack(fill="x", pady=(0, 8))
        OmnitrixCanvas(hdr, 60).pack(side="left", padx=(0, 12))

        tf = tk.Frame(hdr, bg="#0D1117")
        tf.pack(side="left", fill="y", pady=4)
        tk.Label(tf, text="BEN 10: PROTECTOR OF EARTH", font=("Arial", 15, "bold"), bg="#0D1117", fg="#FFFFFF").pack(anchor="w")
        tk.Label(tf, text="REMASTERED PC EDITION  |  60 FPS WIDESCREEN", font=("Arial", 8, "bold"), bg="#0D1117", fg="#39FF14").pack(anchor="w")

        self.nb = ttk.Notebook(left_col)
        self.nb.pack(fill="both", expand=True)
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        t1 = ttk.Frame(self.nb, style="Dark.TFrame")
        t2 = ttk.Frame(self.nb, style="Dark.TFrame")
        t3 = ttk.Frame(self.nb, style="Dark.TFrame")
        self.nb.add(t1, text="  PLAY  ")
        self.nb.add(t2, text="  SETTINGS  ")
        self.nb.add(t3, text="  CONTROLS  ")

        # Tab 1: PLAY
        c1 = ttk.Frame(t1, style="Card.TFrame", padding=16)
        c1.pack(fill="both", expand=True, pady=(8, 0))
        tk.Label(c1, text="GAME DATA FILE (.ISO / .CSO)", font=("Arial", 9, "bold"), bg="#161B22", fg="#8B949E").pack(anchor="w")

        rf = tk.Frame(c1, bg="#0D1117", padx=10, pady=8)
        rf.pack(fill="x", pady=(6, 12))
        self.lbl_rom = tk.Label(rf, text=self._rom_txt(), font=("Arial", 9), bg="#0D1117", fg="#E6EDF3", wraplength=380, justify="left")
        self.lbl_rom.pack(side="left", fill="x", expand=True)
        tk.Button(rf, text="SELECT FILE", font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=10, pady=5, command=self._pick_rom).pack(side="right")

        info_text = (
            "• Native 16:9 Widescreen & 60 FPS unlock ready\n"
            "• Ultra-lightweight engine for old laptops & modern PCs\n"
            "• Full Keyboard + Mouse & XInput Gamepad support\n"
            "• Dynamic art showcase & custom wallpaper support"
        )
        tk.Label(c1, text=info_text, font=("Arial", 9), bg="#161B22", fg="#8B949E", justify="left").pack(anchor="w", pady=(0, 12))

        self.btn_play = tk.Button(c1, text="▶  PLAY GAME", font=("Arial", 13, "bold"), bg="#39FF14", fg="#0D1117", relief="flat", pady=11, command=self._play)
        self.btn_play.pack(side="bottom", fill="x")

        # Tab 2: SETTINGS & CUSTOMIZATION
        c2 = ttk.Frame(t2, style="Card.TFrame", padding=14)
        c2.pack(fill="both", expand=True, pady=(8, 0))

        tk.Label(c2, text="INPUT PROFILE", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14").pack(anchor="w")
        self.v_ctrl = tk.StringVar(value=self.cfg["control_scheme"])
        for txt, val in [("Keyboard + Mouse (WASD + Click Attacks)", "keyboard_mouse"), ("Xbox / PlayStation Controller (XInput)", "gamepad")]:
            ttk.Radiobutton(c2, text=txt, variable=self.v_ctrl, value=val, style="Dark.TRadiobutton", command=self._save_opts).pack(anchor="w")

        tk.Label(c2, text="RENDER RESOLUTION", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14").pack(anchor="w", pady=(8, 1))
        self.v_res = tk.StringVar(value=str(self.cfg["resolution"]))
        rf2 = tk.Frame(c2, bg="#161B22")
        rf2.pack(anchor="w")
        self.res_btns = []
        for txt, val in [("Native", "1"), ("720p", "2"), ("1080p", "3"), ("4K", "6")]:
            rb = ttk.Radiobutton(rf2, text=txt, variable=self.v_res, value=val, style="Dark.TRadiobutton", command=self._save_opts)
            rb.pack(side="left", padx=(0, 12))
            self.res_btns.append(rb)

        tk.Label(c2, text="PERFORMANCE & DISPLAY", font=("Arial", 8, "bold"), bg="#161B22", fg="#39FF14").pack(anchor="w", pady=(8, 1))
        self.v_fps60 = tk.BooleanVar(value=self.cfg.get("fps_60", True))
        self.v_lowpc = tk.BooleanVar(value=self.cfg.get("low_end_pc", False))
        self.v_fs = tk.BooleanVar(value=self.cfg.get("fullscreen", True))
        self.v_vs = tk.BooleanVar(value=self.cfg.get("vsync", False))

        ttk.Checkbutton(c2, text="Unlock 60 FPS Mode (Recommended)", variable=self.v_fps60, style="Dark.TCheckbutton", command=self._save_opts).pack(anchor="w")
        ttk.Checkbutton(c2, text="Low-End / Old PC Mode (Native Res & Fast Speed)", variable=self.v_lowpc, style="Dark.TCheckbutton", command=self._on_low_pc_toggle).pack(anchor="w")
        ttk.Checkbutton(c2, text="Fullscreen Mode (16:9 Widescreen)", variable=self.v_fs, style="Dark.TCheckbutton", command=self._save_opts).pack(anchor="w")
        ttk.Checkbutton(c2, text="Enable VSync", variable=self.v_vs, style="Dark.TCheckbutton", command=self._save_opts).pack(anchor="w")

        art_bar = tk.Frame(c2, bg="#0D1117", padx=8, pady=6)
        art_bar.pack(fill="x", side="bottom", pady=(6, 0))
        tk.Label(art_bar, text="LAUNCHER ART:", font=("Arial", 8, "bold"), bg="#0D1117", fg="#8B949E").pack(side="left")
        tk.Button(art_bar, text="RESET", font=("Arial", 8, "bold"), bg="#21262D", fg="#C9D1D9", relief="flat", padx=8, pady=3, command=self._reset_custom_art).pack(side="right", padx=(6, 0))
        tk.Button(art_bar, text="CUSTOM PHOTO", font=("Arial", 8, "bold"), bg="#21262D", fg="#39FF14", relief="flat", padx=8, pady=3, command=self._pick_custom_art).pack(side="right")

        # Tab 3: CONTROLS
        c3 = ttk.Frame(t3, style="Card.TFrame", padding=16)
        c3.pack(fill="both", expand=True, pady=(8, 0))
        keys = [
            ("W A S D", "Move Character"),
            ("SPACEBAR", "Jump / Double Jump"),
            ("LEFT CLICK", "Light Attack"),
            ("RIGHT CLICK", "Heavy Attack"),
            ("LEFT SHIFT", "Block / Grab / Interact"),
            ("Q / E", "Transform / Cycle Alien Forms"),
            ("ESC / TAB", "Pause / Upgrades Menu")
        ]
        for k, desc in keys:
            row = tk.Frame(c3, bg="#161B22")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=k, font=("Consolas", 9, "bold"), bg="#0D1117", fg="#39FF14", width=16).pack(side="left", padx=(0, 10))
            tk.Label(row, text=desc, font=("Arial", 9), bg="#161B22", fg="#C9D1D9").pack(side="left")

        # Right column: Dynamic Art Showcase
        right_frame = tk.Frame(main_wrap, bg="#39FF14", padx=2, pady=2)
        right_frame.pack(side="right", fill="y")
        self.art_canvas = tk.Canvas(right_frame, width=self.ART_W, height=self.ART_H, bg="#161B22", highlightthickness=0)
        self.art_canvas.pack()

    def _load_pil_art(self, path):
        if not HAS_PIL or not path or not os.path.exists(path):
            return None
        try:
            img = Image.open(path).convert("RGB")
            img = img.resize((self.ART_W, self.ART_H), Image.Resampling.LANCZOS)
            return img
        except Exception:
            return None

    def _switch_art_for_tab(self, tab_idx, instant=False):
        custom = self.cfg.get("custom_art", "")
        if custom and os.path.exists(custom):
            target_path = custom
        else:
            art_name = "art_play.png" if tab_idx == 0 else "art_settings.png"
            target_path = resource_path(os.path.join("assets", art_name))

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
            start_img = self.current_pil
            self._animate_fade(start_img, target_img, step=1, total_steps=8)

    def _animate_fade(self, img1, img2, step, total_steps):
        alpha = step / float(total_steps)
        blended = Image.blend(img1, img2, alpha)
        self.tk_photo = ImageTk.PhotoImage(blended)
        self.art_canvas.delete("all")
        self.art_canvas.create_image(0, 0, anchor="nw", image=self.tk_photo)
        if step < total_steps:
            self._fade_job = self.root.after(28, lambda: self._animate_fade(img1, img2, step + 1, total_steps))
        else:
            self.current_pil = img2
            self._fade_job = None

    def _on_tab_changed(self, _event):
        idx = self.nb.index(self.nb.select())
        self._switch_art_for_tab(idx, instant=False)

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
        state = "disabled" if is_low else "normal"
        for rb in self.res_btns:
            rb.configure(state=state)
        if is_low:
            self.v_res.set("1")

    def _on_low_pc_toggle(self):
        self._sync_low_pc_state()
        self._save_opts()

    def _rom_txt(self):
        p = self.cfg.get("game_path", "")
        return f"Loaded: {os.path.basename(p)}" if p and os.path.exists(p) else "No game data selected (.iso / .cso)"

    def _pick_rom(self):
        p = filedialog.askopenfilename(filetypes=[("PSP Game Data", "*.iso *.cso"), ("All", "*.*")])
        if p:
            self.cfg["game_path"] = p
            ConfigManager.save(self.cfg)
            self.lbl_rom.config(text=self._rom_txt())

    def _save_opts(self):
        self.cfg.update({
            "control_scheme": self.v_ctrl.get(),
            "resolution": self.v_res.get(),
            "fullscreen": self.v_fs.get(),
            "vsync": self.v_vs.get(),
            "fps_60": self.v_fps60.get(),
            "low_end_pc": self.v_lowpc.get()
        })
        ConfigManager.save(self.cfg)

    def _play(self):
        gp = self.cfg.get("game_path", "")
        if not gp or not os.path.exists(gp):
            messagebox.showwarning("Missing Game Data", "Please select your game image file (.iso / .cso) first!")
            return

        self.btn_play.configure(state="disabled", text="LAUNCHING...")
        self.root.update_idletasks()

        try:
            ConfigManager.apply_settings(self.cfg)
            exe = os.path.join(BASE_DIR, "Engine", "Ben10Game.exe")
            if not sys.platform.startswith("win"):
                messagebox.showinfo("Test OK", f"Remastered PC Config written!\n60 FPS: {self.cfg['fps_60']}")
                self.btn_play.configure(state="normal", text="▶  PLAY GAME")
                return
            if not os.path.exists(exe):
                messagebox.showerror("Engine Missing", "Core game files not found inside 'Engine' folder.")
                self.btn_play.configure(state="normal", text="▶  PLAY GAME")
                return
            subprocess.Popen([exe, "--fullscreen", gp])
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to start game:\n{e}")
            self.btn_play.configure(state="normal", text="▶  PLAY GAME")


if __name__ == "__main__":
    root = tk.Tk()
    Ben10RemasteredApp(root)
    root.mainloop()
        
