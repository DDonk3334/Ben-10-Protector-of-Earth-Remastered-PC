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
        "subtitle": "REMASTERED PC EDITION  |  60 FPS WIDESCREEN",
        "playtime": "PLAYTIME: {h}h {m}m",
        "tab_play": "  PLAY  ",
        "tab_settings": "  SETTINGS  ",
        "tab_controls": "  CONTROLS  ",
        "game_data": "GAME DATA FILE (.ISO / .CSO)",
        "select_file": "SELECT FILE",
        "no_rom": "No game data selected (.iso / .cso)",
        "loaded": "Loaded: ",
        "mods_lbl": "MODS & ADD-ONS:",
        "install_mod": "+ INSTALL MOD",
        "clear_mods": "CLEAR MODS",
        "mod_warn": "⚠ Warning: Adding mods, cheats, or custom content may break the game.\nMake sure your mod is stable, as this uses the PSP version.",
        "play_btn": "▶  PLAY GAME",
        "launching": "RUNNING...",
        "input_prof": "INPUT PROFILE",
        "kb_mouse": "Keyboard + Mouse (WASD + Click Attacks)",
        "gamepad": "Xbox / PlayStation Controller (XInput)",
        "res_lbl": "RENDER RESOLUTION",
        "native": "Native",
        "perf_lbl": "PERFORMANCE & DISPLAY",
        "fps60": "Unlock 60 FPS Mode (Recommended)",
        "lowpc": "Low-End / Old PC Mode (Native Res & Fast Speed)",
        "fs": "Fullscreen Mode (16:9 Widescreen)",
        "vsync": "Enable VSync",
        "saves_lbl": "SAVE STATES:",
        "bkp_btn": "BACKUP",
        "rst_save_btn": "RESTORE",
        "bkp_ok": "Save states & progress backed up to SaveStates_Backup.zip!",
        "rst_ok": "Save states restored successfully!",
        "rst_miss": "No backup file (SaveStates_Backup.zip) found yet.",
        "art_lbl": "WALLPAPER:",
        "custom_art": "CUSTOM PHOTO",
        "reset_art": "RESET",
        "mod_ok": "Mod installed: ",
        "clear_ask": "Remove all installed mods and cheats and restore original files?",
        "clear_ok": "All mods removed!",
        "miss_rom": "Please select your game image file (.iso / .cso) first!",
        "keys": [
            ("W A S D", "Move Character"),
            ("SPACEBAR", "Jump / Double Jump"),
            ("LEFT CLICK / J", "Light Attack"),
            ("RIGHT CLICK / K", "Heavy Attack"),
            ("LEFT SHIFT / L", "Block / Grab / Interact"),
            ("1 2 3 4 / ARROWS", "Select Alien Form"),
            ("Q / E", "Omnitrix / Camera"),
            ("F5 / F7", "Quick Save State / Load State"),
            ("ESC / TAB", "Pause / Upgrades Menu")
        ]
    },
    "ru": {
        "subtitle": "REMASTERED PC EDITION  |  60 FPS ШИРОКИЙ ЭКРАН",
        "playtime": "В ИГРЕ: {h} ч {m} м",
        "tab_play": "  ИГРАТЬ  ",
        "tab_settings": "  НАСТРОЙКИ  ",
        "tab_controls": "  УПРАВЛЕНИЕ  ",
        "game_data": "ОБРАЗ ИГРЫ (.ISO / .CSO)",
        "select_file": "ВЫБРАТЬ ФАЙЛ",
        "no_rom": "Файл игры не выбран (.iso / .cso)",
        "loaded": "Выбран: ",
        "mods_lbl": "МОДЫ И ДОПОЛНЕНИЯ:",
        "install_mod": "+ ПОСТАВИТЬ МОД",
        "clear_mods": "УДАЛИТЬ МОДЫ",
        "mod_warn": "⚠ Внимание: добавление модов, читов и любого контента может сломать игру.\nСледите за тем, чтобы мод был стабильным, так как это PSP-версия.",
        "play_btn": "▶  ЗАПУСТИТЬ ИГРУ",
        "launching": "ИГРА ЗАПУЩЕНА...",
        "input_prof": "УСТРОЙСТВО УПРАВЛЕНИЯ",
        "kb_mouse": "Клавиатура + Мышь (WASD + Клики атаки)",
        "gamepad": "Геймпад Xbox / PlayStation (XInput)",
        "res_lbl": "РАЗРЕШЕНИЕ ГРАФИКИ",
        "native": "Родное",
        "perf_lbl": "ПРОИЗВОДИТЕЛЬНОСТЬ И ЭКРАН",
        "fps60": "Разблокировать 60 FPS (Рекомендуется)",
        "lowpc": "Режим для слабых ПК (Родное разрешение и скорость)",
        "fs": "Полноэкранный режим (16:9)",
        "vsync": "Вертикальная синхронизация (VSync)",
        "saves_lbl": "СЕЙВ-СТЕЙТЫ:",
        "bkp_btn": "БЭКАП",
        "rst_save_btn": "ВОССТАНОВИТЬ",
        "bkp_ok": "Сейв-стейты и сохранения сохранены в SaveStates_Backup.zip!",
        "rst_ok": "Сейв-стейты успешно восстановлены!",
        "rst_miss": "Файл резервной копии (SaveStates_Backup.zip) пока не найден.",
        "art_lbl": "ФОН:",
        "custom_art": "СВОЁ ФОТО",
        "reset_art": "СБРОС",
        "mod_ok": "Мод установлен: ",
        "clear_ask": "Удалить все установленные моды и вернуть игру к оригиналу?",
        "clear_ok": "Все моды удалены!",
        "miss_rom": "Сначала выберите файл образа игры (.iso / .cso)!",
        "keys": [
            ("W A S D", "Движение персонажа"),
            ("ПРОБЕЛ", "Прыжок / Двойной прыжок"),
            ("ЛКМ / J", "Лёгкая атака"),
            ("ПКМ / K", "Сильная атака"),
            ("LEFT SHIFT / L", "Блок / Захват / Действие"),
            ("1 2 3 4 / СТРЕЛКИ", "Выбор пришельца"),
            ("Q / E", "Омнитрикс / Камера"),
            ("F5 / F7", "Быстрый сейв-стейт / Загрузка"),
            ("ESC / TAB", "Пауза / Меню улучшений")
        ]
    },
    "de": {
        "subtitle": "REMASTERED PC EDITION  |  60 FPS BREITBILD",
        "playtime": "SPIELZEIT: {h}h {m}m",
        "tab_play": "  SPIELEN  ",
        "tab_settings": "  EINSTELLUNGEN  ",
        "tab_controls": "  STEUERUNG  ",
        "game_data": "SPIELDATEI (.ISO / .CSO)",
        "select_file": "DATEI WÄHLEN",
        "no_rom": "Keine Spieldatei gewählt (.iso / .cso)",
        "loaded": "Geladen: ",
        "mods_lbl": "MODS & ADD-ONS:",
        "install_mod": "+ MOD INSTALLIEREN",
        "clear_mods": "MODS LÖSCHEN",
        "mod_warn": "⚠ Achtung: Mods, Cheats oder fremde Inhalte können das Spiel beschädigen.\nAchte auf stabile Mods, da dies die PSP-Version ist.",
        "play_btn": "▶  SPIEL STARTEN",
        "launching": "LÄUFT...",
        "input_prof": "STEUERUNGSPROFIL",
        "kb_mouse": "Tastatur + Maus (WASD + Mausklicks)",
        "gamepad": "Xbox / PlayStation Controller (XInput)",
        "res_lbl": "AUFLÖSUNG",
        "native": "Nativ",
        "perf_lbl": "LEISTUNG & ANZEIGE",
        "fps60": "60 FPS Modus freischalten (Empfohlen)",
        "lowpc": "Schwacher PC Modus (Native Auflösung & Tempo)",
        "fs": "Vollbildmodus (16:9 Breitbild)",
        "vsync": "VSync aktivieren",
        "saves_lbl": "SAVE STATES:",
        "bkp_btn": "BACKUP",
        "rst_save_btn": "LADEN",
        "bkp_ok": "Save States erfolgreich in SaveStates_Backup.zip gesichert!",
        "rst_ok": "Save States wiederhergestellt!",
        "rst_miss": "Kein Backup (SaveStates_Backup.zip) gefunden.",
        "art_lbl": "BILD:",
        "custom_art": "EIGENES FOTO",
        "reset_art": "RESET",
        "mod_ok": "Mod installiert: ",
        "clear_ask": "Alle installierten Mods entfernen und Originalzustand wiederherstellen?",
        "clear_ok": "Alle Mods entfernt!",
        "miss_rom": "Bitte wähle zuerst deine Spieldatei (.iso / .cso) aus!",
        "keys": [
            ("W A S D", "Charakter bewegen"),
            ("LEERTASTE", "Springen / Doppelsprung"),
            ("LINKSKLICK / J", "Leichter Angriff"),
            ("RECHTSKLICK / K", "Starker Angriff"),
            ("LINKS SHIFT / L", "Blocken / Greifen"),
            ("1 2 3 4 / PFEILE", "Alien auswählen"),
            ("Q / E", "Omnitrix / Kamera"),
            ("F5 / F7", "Schnellspeichern / Schnellladen"),
            ("ESC / TAB", "Pause / Upgrades")
        ]
    },
    "ja": {
        "subtitle": "REMASTERED PC EDITION  |  60 FPS ワイド画面",
        "playtime": "プレイ時間: {h}時間 {m}分",
        "tab_play": "  プレイ  ",
        "tab_settings": "  設定  ",
        "tab_controls": "  操作方法  ",
        "game_data": "ゲームデータ (.ISO / .CSO)",
        "select_file": "ファイル選択",
        "no_rom": "ゲームファイル未選択 (.iso / .cso)",
        "loaded": "選択済み: ",
        "mods_lbl": "MOD・追加コンテンツ:",
        "install_mod": "+ MOD導入",
        "clear_mods": "MOD削除",
        "mod_warn": "⚠ 注意: MODやチートの導入によりゲームが破損する場合があります。\nPSP版ベースのため、安定したMODを使用してください。",
        "play_btn": "▶  ゲーム開始",
        "launching": "起動中...",
        "input_prof": "操作デバイス",
        "kb_mouse": "キーボード + マウス (WASD + クリック攻撃)",
        "gamepad": "Xbox / PlayStation コントローラー (XInput)",
        "res_lbl": "描画解像度",
        "native": "標準",
        "perf_lbl": "パフォーマンスと画面設定",
        "fps60": "60 FPS モードを有効化 (推奨)",
        "lowpc": "低スペックPCモード (標準解像度・高速化)",
        "fs": "フルスクリーンモード (16:9 ワイド)",
        "vsync": "垂直同期 (VSync)",
        "saves_lbl": "ステートセーブ:",
        "bkp_btn": "保存",
        "rst_save_btn": "復元",
        "bkp_ok": "ステートセーブを SaveStates_Backup.zip に保存しました！",
        "rst_ok": "ステートセーブを復元しました！",
        "rst_miss": "バックアップファイルが見つかりません。",
        "art_lbl": "背景:",
        "custom_art": "画像変更",
        "reset_art": "リセット",
        "mod_ok": "MODを導入しました: ",
        "clear_ask": "導入済みのMODをすべて削除して初期状態に戻しますか？",
        "clear_ok": "すべてのMODを削除しました！",
        "miss_rom": "先にゲームファイル (.iso / .cso) を選択してください！",
        "keys": [
            ("W A S D", "移動"),
            ("SPACE", "ジャンプ / 二段ジャンプ"),
            ("左クリック / J", "弱攻撃"),
            ("右クリック / K", "強攻撃"),
            ("LEFT SHIFT / L", "ガード / つかむ / 調べる"),
            ("1 2 3 4 / 矢印キー", "エイリアン変身選択"),
            ("Q / E", "オムニトリックス / カメラ"),
            ("F5 / F7", "クイックセーブ / クイックロード"),
            ("ESC / TAB", "ポーズ / アップグレード")
        ]
    }
}


class OmnitrixCanvas(tk.Canvas):
    def __init__(self, parent, size=58):
        super().__init__(parent, width=size, height=size, bg="#0D1117", highlightthickness=0)
        p = 5
        self.create_oval(p, p, size - p, size - p, fill="#161B22", outline="#39FF14", width=3)
        self.create_polygon(p + 10, p + 7, size - p - 10, p + 7, size // 2, size // 2, fill="#39FF14")
        
