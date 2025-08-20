import time
print(f"[{time.time()}] App start (main)")
import sys
import threading
import requests
import packaging.version
import os
import webbrowser
import psutil
import tempfile
import ctypes
if sys.platform == "win32":
    import winreg
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
        QPushButton, QMessageBox, QSystemTrayIcon, QMenu, QAction, QDialog, QGraphicsDropShadowEffect, QFrame  
        )
    from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer, QStandardPaths, QCoreApplication
    from PyQt5.QtGui import QFont, QIcon, QPainter, QColor, QBrush, QPixmap, QLinearGradient, QPen
    from PyQt5.QtNetwork import QLocalServer, QLocalSocket
    from tooltip import CivTooltip
    print(f"[{time.time()}] Imports complete")
ACCENT = "#CDE6FF"           # subtle cyan accent
FG     = "#EAF2F9"           # primary text
MUTED  = "#AFC4D8"           # headers/subtext
GLASS_GRAD_A = (42, 45, 55, 165)
GLASS_GRAD_B = (30, 33, 43, 165)
BORDER_RGBA  = (255, 255, 255, 18) # subtle 1px border
RADIUS = 18

PROFILE_FILE = "profile_id.txt"
POLL_INTERVAL = 15  # seconds
HEADERS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
"Accept": "application/json",
"Referer": "https://aoe2companion.com"
}
DEFAULT_FONT_SIZE = 9
CURRENT_VERSION = "1.1.4"  # Update this for each release
GITHUB_API_LATEST_RELEASE = "https://api.github.com/repos/BubbleDuckz/AgeofDuck-ELO-Overlay-for-Age-of-Empires-2-DE/releases/latest"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DATA_DIR = os.path.join(
    QStandardPaths.writableLocation(QStandardPaths.AppDataLocation),
    "AgeOfDuck"
    )
UPDATE_FLAG_PATH = os.path.join(tempfile.gettempdir(), "AgeOfDuck_updated.flag")
os.makedirs(APP_DATA_DIR, exist_ok=True)

PROFILE_FILE = os.path.join(APP_DATA_DIR, "profile_id.txt")
POSITION_FILE = os.path.join(APP_DATA_DIR, "overlay_position.txt")

def get_app_startup_path():
    app_name = "AgeOfDuck"
    exe_path = f'"{os.path.join(APP_DIR, "AgeOfDuck.exe")}"'
    return app_name, exe_path

    def set_app_startup(enable=True):
        if sys.platform != "win32":
            return
            app_name, exe_path = get_app_startup_path()
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_ALL_ACCESS
                )
            if enable:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass
                    winreg.CloseKey(key)

                    def is_app_startup_enabled():
                        if sys.platform != "win32":
                            return False
                            app_name, exe_path = get_app_startup_path()
                            try:
                                key = winreg.OpenKey(
                                    winreg.HKEY_CURRENT_USER,
                                    r"Software\Microsoft\Windows\CurrentVersion\Run"
                                    )
                                value, _ = winreg.QueryValueEx(key, app_name)
                                winreg.CloseKey(key)
                                return exe_path in value
                            except FileNotFoundError:
                                return False


                                def check_for_update():
                                    try:
                                        r = requests.get(GITHUB_API_LATEST_RELEASE, timeout=8)
                                        r.raise_for_status()
                                        data = r.json()
                                        latest = (data.get("tag_name") or "").lstrip("v")
                                        if latest and packaging.version.parse(latest) > packaging.version.parse(CURRENT_VERSION):
                                            installer_url = None
                                            for asset in data.get("assets", []):
                                                name = asset["name"].lower()
                                                if "installer" in name or name.endswith("-setup.exe"):
                                                    installer_url = asset["browser_download_url"]
                                                    break
                                                    return latest, installer_url
                                                except Exception as e:
                                                    print("Update check failed:", e)
                                                    return None, None

                                                    def download_and_run_installer(installer_url, tray_icon):
                                                        from PyQt5.QtWidgets import QApplication
                                                        import tempfile, requests, os, ctypes

                                                        if not installer_url:
                                                            tray_icon.showMessage("Update Error", "Installer URL not found.", QSystemTrayIcon.Critical)
                                                            return

                                                            try:
                                                                temp_installer = os.path.join(tempfile.gettempdir(), "AgeOfDuckInstaller.exe")
                                                                tray_icon.showMessage("Updating", "Downloading installer…", QSystemTrayIcon.Information)
                                                                with requests.get(installer_url, stream=True, timeout=60) as r:
                                                                    r.raise_for_status()
                                                                    with open(temp_installer, "wb") as f:
                                                                        for chunk in r.iter_content(8192):
                                                                            if chunk:
                                                                                f.write(chunk)
                                                                                log_path = os.path.join(tempfile.gettempdir(), "AgeOfDuck_Install.log")
                                                                                params = f'/LOG="{log_path}" /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS'
                                                                                open(UPDATE_FLAG_PATH, "w").close()
                                                                                ctypes.windll.shell32.ShellExecuteW(None, "runas", temp_installer, params, None, 1)
                                                                                tray_icon.showMessage("Updating", "Installer launched. The app will close and restart automatically.", QSystemTrayIcon.Information)

                                                                            except Exception as e:
                                                                                tray_icon.showMessage("Update Error", f"{e}", QSystemTrayIcon.Critical)





                                                                                def is_another_instance_running(server_name="AgeOfDuckOverlaySingleton"):
                                                                                    socket = QLocalSocket()
                                                                                    socket.connectToServer(server_name)
                                                                                    if socket.waitForConnected(1000):
                                                                                        socket.close()
                                                                                        return True
                                                                                    else:
                                                                                        server = QLocalServer()
                                                                                        try:
                                                                                            QLocalServer.removeServer(server_name)
                                                                                        except Exception:
                                                                                            pass
                                                                                            if not server.listen(server_name):
                                                                                                return True
                                                                                                return server

                                                                                                def resource_path(relative_path):
                                                                                                    """ Get absolute path to resource, works for dev and PyInstaller """
                                                                                                    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

        def fetch_live_match(profile_id):
            print(f"[{time.time()}] fetch_live_match({profile_id}) called")
            start = time.time()
            url = (
                "https://data.aoe2companion.com/api/matches"
                "?direction=forward"
                f"&profile_ids={profile_id}"
                "&with_profile_ids="
                "&search="
                "&leaderboard_ids="
                "&use_enums=true"
                "&page=1"
                "&language=en"
                )
            try:
                r = requests.get(url, headers=HEADERS, timeout=8)
                if r.status_code != 200:
                    print(f"Live match API error: HTTP {r.status_code}")
                    return None
                    data = r.json()
                    for match in data.get("matches", []):
                        if match.get("finished") is None:
                            return match
                        except Exception as e:
                            print("Error fetching live match:", e)
                            return None

                            def fetch_player_elo(profile_id, leaderboard_id):
                                print(f"[{time.time()}] fetch_player_elo({profile_id}, {leaderboard_id}) called")
                                url = f"https://data.aoe2companion.com/api/profiles/{profile_id}?page=1&language=en"
                                try:
                                    r = requests.get(url, headers=HEADERS, timeout=8)
                                    if r.status_code != 200:
                                        print(f"Player profile API error: HTTP {r.status_code}")
                                        return None, None
                                        data = r.json()
                                        for lb in data.get("leaderboards", []):
                                            if lb["leaderboardId"] == leaderboard_id:
                                                return lb.get("rating"), lb.get("maxRating")
                                            except Exception as e:
                                                print("Error fetching elo:", e)
                                                return None, None

                                                def fetch_all_players_elos(match):
                                                    print(f"[{time.time()}] fetch_all_players_elos called")
                                                    leaderboard_id = match.get('leaderboardId')
                                                    out = []
                                                    for team in match.get('teams', []):
                                                        team_id = team.get("teamId")
                                                        for player in team.get("players", []):
                                                            pid = player["profileId"]
                                                            name = player.get("name")
                                                            color = player.get("colorHex", "#888888")
                                                            civ = player.get("civName", "")
                                                            country = player.get("country", "")
                                                            rating, peak = fetch_player_elo(pid, leaderboard_id)
                                                            out.append({
                                                                "name": name,
                                                                "team": team_id,
                                                                "color": color,
                                                                "civ": civ,
                                                                "country": country,
                                                                "rating": rating,
                                                                "peak": peak,
                                                                "profile_id": pid,
                                                                })
                                                            return out

                                                            def save_last_profile_id(profile_id):
                                                                try:
                                                                    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
                                                                        f.write(profile_id.strip())
                                                                    except Exception:
                                                                        pass

                                                                        def load_last_profile_id():
                                                                            start = time.time()
                                                                            print(f"[{start}] load_last_profile_id called")
                                                                            result = ""
                                                                            try:
                                                                                if os.path.exists(PROFILE_FILE):
                                                                                    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                                                                                        result = f.read().strip()
                                                                                    except Exception as e:
                                                                                        print(f"[{time.time()}] Exception in load_last_profile_id: {e}")
                                                                                        end = time.time()
                                                                                        print(f"[{end}] load_last_profile_id returning: '{result}' (took {end-start:.4f}s)")
                                                                                        return result

                                                                                        class Worker(QObject):

                                                                                            data_updated = pyqtSignal(dict, list, str, str)
                                                                                            not_in_game = pyqtSignal()
                                                                                            profile_error = pyqtSignal(str)
                                                                                            set_loading = pyqtSignal(bool)
    in_game_signal = pyqtSignal(bool)  # New signal: True = in game, False = not in game

    def __init__(self):
        super().__init__()
        print(f"[{time.time()}] Worker __init__")
        self.running = True
        self.profile_id = None
        self.display_name = None
        self.aoe2_running = False   
        self._last_in_game_state = None  # Track last state to avoid redundant emits

        def set_game_running_state(self, running):
            self.aoe2_running = running

            def set_profile(self, profile_id):
                print(f"[{time.time()}] Worker.set_profile called with profile_id={profile_id}")
                if not profile_id or not profile_id.strip().isdigit():
                    self.profile_error.emit("Please enter a valid numeric profile ID.")
                    return
                    self.profile_id = profile_id.strip()
                    self.display_name = profile_id.strip()
        self.set_loading.emit(False) # This signal is connected but its slot in Overlay is 'pass'
        print(f"[{time.time()}] Worker profile_id set to {self.profile_id}")

        def poll_loop(self):
            print(f"[{time.time()}] Worker thread starting poll_loop")
            while self.running:
                print(f"[{time.time()}] Worker: aoe2_running={self.aoe2_running}, profile_id={self.profile_id}, running={self.running}")

            in_game = False  # default

            if not self.aoe2_running:
                if self._last_in_game_state is not False:
                    self.in_game_signal.emit(False)
                    self.not_in_game.emit()   # transition to 'not in game'
                    self._last_in_game_state = False
                    time.sleep(1)
                    continue

                    if not self.profile_id:
                        if self._last_in_game_state is not False:
                            self.in_game_signal.emit(False)
                            self.not_in_game.emit()
                            self._last_in_game_state = False
                            time.sleep(0.5)
                            continue

                            match = fetch_live_match(self.profile_id)
                            if match:
                                in_game = True
                                game_mode = match.get("leaderboardName", "?")
                                map_name  = match.get("mapName", "?")
                                try:
                                    players = fetch_all_players_elos(match)
                                except Exception as e:
                                    print(f"Error fetching all players elos: {e}")
                                    players = []

                                    self.data_updated.emit(match, players, game_mode, map_name)
                                else:
                                    in_game = False
                                    if self._last_in_game_state != in_game:
                                        self.in_game_signal.emit(in_game)
                                        if not in_game:
                    self.not_in_game.emit()  # only on transition into 'not in game'
                    self._last_in_game_state = in_game

                    for _ in range(POLL_INTERVAL):
                        if not self.running:
                            return
                            time.sleep(1)


                            class ProcessChecker(QObject):
                                aoe2_running_changed = pyqtSignal(bool)

                                def __init__(self):
                                    super().__init__()
                                    self._running = True
                                    self._last_state = None

                                    def stop(self):
                                        self._running = False

                                        def run(self):
                                            while self._running:
                                                aoe_running = False
                                                try:
                                                    for p in psutil.process_iter(['name']):
                                                        try:
                                                            if (p.info['name'] or '').lower() == "aoe2de_s.exe":
                                                                aoe_running = True
                                                                break
                                                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                                                continue
                                                            except Exception:
                                                                pass

                                                                if aoe_running != self._last_state:
                                                                    self.aoe2_running_changed.emit(aoe_running)
                                                                    self._last_state = aoe_running

            time.sleep(2)  # Sleep 2 seconds between checks

            class SettingsWindow(QWidget):
                profile_set = pyqtSignal(str)

                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("Set Profile ID")
                    self.setFixedSize(280, 150)
                    self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
                    layout = QVBoxLayout(self)
                    label = QLabel("Enter Numeric AoE2 Profile ID:")
                    label.setStyleSheet("color:#222; font-size:14px;")
                    self.edit = QLineEdit()
                    self.edit.setStyleSheet("background:#fff; color:#222; font-size:16px;")
                    self.btn_set = QPushButton("Set")
                    self.btn_help = QPushButton("Help to find my Profile ID Number")
                    self.btn_help.setStyleSheet("font-size:14px;")
                    self.btn_help.clicked.connect(self.show_help)
                    self.btn_set.setStyleSheet("font-size:14px;")
                    self.btn_set.clicked.connect(self.set_profile)
                    self.edit.returnPressed.connect(self.set_profile)
                    layout.addWidget(label)
                    layout.addWidget(self.edit)
                    layout.addWidget(self.btn_help)
                    layout.addWidget(self.btn_set)
                    self.edit.setText(load_last_profile_id())

                    def show_help(self):
                        webbrowser.open("https://www.aoe2insights.com")
                        dlg = QDialog(self)
                        dlg.setWindowTitle("How to find your Profile ID")
                        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint)
                        layout = QVBoxLayout(dlg)

                        label_text = QLabel(
                            "1. Search your in-game username.<br>"
                            "2. Click your profile from the list.<br>"
                            "3. Your Profile ID will appear in the URL and on your profile page.<br><br>"
                            "<i>Example below:</i>"
                            )
                        label_text.setWordWrap(True)
                        label_text.setTextFormat(Qt.RichText)
                        layout.addWidget(label_text)

                        pix = QPixmap(resource_path("profile.png"))
                        if not pix.isNull():
                            label_img = QLabel()
                            label_img.setPixmap(pix.scaledToWidth(350, Qt.SmoothTransformation))
                            layout.addWidget(label_img)
                        else:
                            layout.addWidget(QLabel("(profile.png not found)"))

                            dlg.setLayout(layout)
                            dlg.setFixedSize(400, 380)
                            dlg.raise_()
                            dlg.activateWindow()
                            dlg.exec_()


                            def set_profile(self):
                                profile_id = self.edit.text().strip()
                                if not profile_id or not profile_id.isdigit():
                                    QMessageBox.warning(self, "Error", "Enter a numeric AoE2 profile ID.")
                                    return
                                    save_last_profile_id(profile_id)
                                    self.profile_set.emit(profile_id)
                                    self.hide()

                                    def show_and_focus(self):
                                        self.edit.setText(load_last_profile_id())
                                        self.show()
                                        self.raise_()
                                        self.activateWindow()
                                        self.edit.setFocus()

                                        class Overlay(QWidget):
                                            game_running_changed = pyqtSignal(bool)
                                            def __init__(self, tray_icon):
                                                start = time.time()
                                                self.is_waiting = True
                                                self._last_civs_sig = None
                                                print(f"[{start}] Overlay __init__ starting")
                                                super().__init__()
        self.scale_factor = 1.0  # 100%
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(12)
        self.setGraphicsEffect(shadow)

        self._aoe2_running = False
        self.setWindowTitle("AoE2 Elo Overlay")
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool # Prevents showing in taskbar
            )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.font_size = DEFAULT_FONT_SIZE
        self.drag = False
        self.last_mouse_pos = None
        self.tray_icon = tray_icon

        self.locked = False
        self._init_ui()
        self.waiting_timer = QTimer()
        self.waiting_timer.timeout.connect(self.animate_waiting)
        self.waiting_dot_count = 1
        self.resize(300, 1) # Made it smaller initially
        self.restore_last_position()

        self.worker = Worker()
        self.worker.in_game_signal.connect(self.on_game_state_changed)
        self.game_running_changed.connect(self.worker.set_game_running_state)
        self.worker_thread = threading.Thread(target=self.worker.poll_loop, daemon=True)
        self.worker.data_updated.connect(self.update_overlay)
        self.worker.not_in_game.connect(self.hide_overlay)
        self.worker.profile_error.connect(self.profile_error)
        self.worker.set_loading.connect(self.set_loading)
        self.worker_thread.start()
        self.showing = False
        self.set_loading(False) # Initial state
        self.process_checker = ProcessChecker()
        self.process_checker.aoe2_running_changed.connect(self.on_aoe2_running_changed)

        self.process_thread = threading.Thread(target=self.process_checker.run, daemon=True)
        self.process_thread.start()
        print(f"[{time.time()}] Overlay __init__ done, took {time.time() - start:.4f}s")

        def _s(self, x: float) -> int:
            return max(1, int(round(x * self.scale_factor)))

            def on_game_state_changed(self, in_game: bool):
                if hasattr(self, 'civ_tooltip'):
                    self.civ_tooltip.set_game_state(in_game)

                    def on_aoe2_running_changed(self, running):
                        self._aoe2_running = running
                        self.game_running_changed.emit(running)
                        if running and not self.isVisible():
                            self.show()
                        elif not running:
                            self.waiting_timer.stop()
                            self.hide()

                            def closeEvent(self, event):
                                self.process_checker.stop()
                                self.process_thread.join(timeout=1)
                                event.accept()

                                def moveEvent(self, event):
                                    super().moveEvent(event)
                                    pos = self.pos()
                                    try:
                                        with open(POSITION_FILE, "w", encoding="utf-8") as f:
                                            f.write(f"{pos.x()},{pos.y()}")
                                        except Exception:
                                            pass

                                            def restore_last_position(self):
                                                try:
                                                    with open(POSITION_FILE, "r", encoding="utf-8") as f:
                                                        coords = f.read().strip().split(",")
                                                        if len(coords) == 2:
                                                            x, y = int(coords[0]), int(coords[1])
                                                            screen = QApplication.primaryScreen().geometry()
                                                            x = max(0, min(screen.width() - self.width(), x))
                                                            y = max(0, min(screen.height() - self.height(), y))
                                                            self.move(x, y)
                                                        except Exception:
                                                            self.move(40, 80)


                                                            def paintEvent(self, event):
                                                                painter = QPainter(self)
                                                                painter.setRenderHint(QPainter.Antialiasing)

                                                                rect = self.rect().adjusted(1, 1, -1, -1)

                                                                grad = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
                                                                grad.setColorAt(0, QColor(*GLASS_GRAD_A))
                                                                grad.setColorAt(1, QColor(*GLASS_GRAD_B))

                                                                painter.setBrush(QBrush(grad))
                                                                painter.setPen(Qt.NoPen)
        radius = self._s(self._BASE_RADIUS)  # <-- scaled
        painter.drawRoundedRect(rect, radius, radius)

        pen = QPen(QColor(*BORDER_RGBA))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)


        def _init_ui(self):
            self.font_size = DEFAULT_FONT_SIZE
            self.outer = QVBoxLayout(self)
            self._BASE_WIDTH = 380
            self._BASE_OUTER_MARGINS = (16, 12, 12, 6)
            self._BASE_ROW_SPACING = 16
        self._BASE_HEADER_MIN = (160, 80, 45, 35)  # name, civ, current, peak
        self._BASE_DIVIDER_H = 2
        self._BASE_DRAG_W = 100
        self._BASE_DRAG_H = 3
        self._BASE_WAIT_MS = 500
        self._BASE_RADIUS = 18  # used by paintEvent
        def add_text_shadow(widget, blur=6, alpha=200):
            eff = QGraphicsDropShadowEffect(self)
            eff.setBlurRadius(blur)
            eff.setOffset(0, 0)
            eff.setColor(QColor(0, 0, 0, alpha))  # dark halo
            widget.setGraphicsEffect(eff)
            self.drag_bar = QWidget(self)
            self.drag_bar.setFixedHeight(self._s(self._BASE_DRAG_H))
            self.drag_bar.setFixedWidth(self._s(self._BASE_DRAG_W))
            self.drag_bar.setStyleSheet("""
                background: rgba(255,255,255,0.6);
                border-radius: 3px;
                """)
            drag_bar_container = QHBoxLayout()
            drag_bar_container.setContentsMargins(0, 0, 0, self._s(6))
            drag_bar_container.addStretch()
            drag_bar_container.addWidget(self.drag_bar)
            drag_bar_container.addStretch()
            self.outer.addLayout(drag_bar_container)

            self.outer.setContentsMargins(
                *[self._s(v) for v in self._BASE_OUTER_MARGINS]
                )
            self.outer.setSpacing(self._s(3))
            self.drag_bar.mousePressEvent = self.drag_bar_mousePressEvent
            self.drag_bar.mouseMoveEvent = self.drag_bar_mouseMoveEvent
            self.drag_bar.mouseReleaseEvent = self.drag_bar_mouseReleaseEvent
            self.top_row = QHBoxLayout()
            self.top_row.setContentsMargins(0, 0, 0, 0)
            self.top_row.setSpacing(10)

            self.label_gamemode = QLabel("Team Random Map")
            self.label_gamemode.setFont(QFont("Segoe UI", self.font_size + 2, QFont.DemiBold))
            self.label_gamemode.setStyleSheet(f"color:{FG}; background:transparent;")
            add_text_shadow(self.label_gamemode, blur=8, alpha=220)

            self.label_map = QLabel("│ Nomad")
            self.label_map.setFont(QFont("Segoe UI", self.font_size + 2))
            self.label_map.setStyleSheet(f"color:{ACCENT}; background:transparent;")
            add_text_shadow(self.label_map, blur=8, alpha=220)

            self.top_row.addWidget(self.label_gamemode)
            self.top_row.addWidget(self.label_map)
            self.top_row.addStretch()
            def make_icon_btn(text):
                b = QPushButton(text)
                b.setFixedSize(20, 20)
                b.setCursor(Qt.PointingHandCursor)
                b.setStyleSheet("""
                    QPushButton {
                    background: rgba(255,255,255,0.08);
                    border: 1px solid rgba(255,255,255,0.10);
                    border-radius: 4px;
                    color: rgba(255,255,255,0.92);
                    font-size: 13px;
                    padding: 0;
                    }
                    QPushButton:hover  { background: rgba(255,255,255,0.12); }
                    QPushButton:pressed{ background: rgba(255,255,255,0.16); }
                    QPushButton:disabled{opacity:0.45;}
                    """)
                return b

                self.btn_font_plus  = make_icon_btn("+")
                self.btn_font_minus = make_icon_btn("–")
                self.btn_lock       = make_icon_btn("🔒" if self.locked else "🔓")

                self.btn_lock.clicked.connect(self.toggle_lock)
                self.top_row.addWidget(self.btn_font_minus)
                self.top_row.addWidget(self.btn_font_plus)
                self.top_row.addWidget(self.btn_lock)

                self.outer.addLayout(self.top_row)
                div = QFrame()
                div.setFrameShape(QFrame.HLine)
                div.setFixedHeight(self._s(self._BASE_DIVIDER_H))
                div.setStyleSheet("color: rgba(255,255,255,0.10);")
                self.outer.addWidget(div)
                self.player_header_layout = QHBoxLayout()
                self.player_header_layout.setContentsMargins(2, 0, 2, 0)
                self.player_header_layout.setSpacing(16)

                def H(text):
                    lbl = QLabel(text)
                    lbl.setFont(QFont("Segoe UI", self.font_size, QFont.DemiBold))
                    lbl.setStyleSheet(f"color:{MUTED}; background:transparent;")
            add_text_shadow(lbl, blur=5, alpha=160)  # subtle for headers
            return lbl

            self.header_name    = H("Name")
            self.header_civ     = H("Civ")
            self.header_current = H("Current")
            self.header_peak    = H("Peak")

            self.header_name.setAlignment(Qt.AlignLeft)
            self.header_civ.setAlignment(Qt.AlignLeft)
            self.header_current.setAlignment(Qt.AlignLeft)
            self.header_peak.setAlignment(Qt.AlignLeft)

            self.header_name.setMinimumWidth(self._s(self._BASE_HEADER_MIN[0]))
            self.header_civ.setMinimumWidth(self._s(self._BASE_HEADER_MIN[1]))
            self.header_current.setMinimumWidth(self._s(self._BASE_HEADER_MIN[2]))
            self.header_peak.setMinimumWidth(self._s(self._BASE_HEADER_MIN[3]))

            self.player_header_layout.addWidget(self.header_name)
            self.player_header_layout.addWidget(self.header_civ)
            self.player_header_layout.addWidget(self.header_current)
            self.player_header_layout.addWidget(self.header_peak)
            self.outer.addLayout(self.player_header_layout)
            self.player_content_layout = QVBoxLayout()
            self.player_content_layout.setContentsMargins(2, 0, 2, 0)
            self.player_content_layout.setSpacing(6)

            self.player_rows = []

            def make_name_label():
                lbl = QLabel("")
            lbl.setFont(QFont("Segoe UI", self.font_size, QFont.DemiBold))  # bold only for Name
            lbl.setStyleSheet(f"color:{FG}; background:transparent;")
            add_text_shadow(lbl, blur=6, alpha=210)
            return lbl

            def make_data_label():
                lbl = QLabel("")
            lbl.setFont(QFont("Segoe UI", self.font_size))                   # regular for Civ/Current/Peak
            lbl.setStyleSheet(f"color:{FG}; background:transparent;")
            add_text_shadow(lbl, blur=6, alpha=210)
            return lbl

            for _ in range(8):
                row = QHBoxLayout()
                row.setSpacing(self._s(self._BASE_ROW_SPACING))

                lbl_name  = make_name_label()
                lbl_civ   = make_data_label()
                lbl_cur   = make_data_label()
                lbl_peak  = make_data_label()

                lbl_name.setMinimumWidth(self.header_name.minimumWidth())
                lbl_civ.setMinimumWidth(self.header_civ.minimumWidth())
                lbl_cur.setMinimumWidth(self.header_current.minimumWidth())
                lbl_peak.setMinimumWidth(self.header_peak.minimumWidth())

                row.addWidget(lbl_name)
                row.addWidget(lbl_civ)
                row.addWidget(lbl_cur)
                row.addWidget(lbl_peak)

                self.player_rows.append({
                    "layout": row,
                    "name_label": lbl_name,
                    "civ_label": lbl_civ,
                    "current_label": lbl_cur,
                    "peak_label": lbl_peak
                    })
                self.player_content_layout.addLayout(row)

                self.outer.addLayout(self.player_content_layout)
                self.outer.addStretch()
                self._update_font_size()
                self.civ_tooltip = CivTooltip(
                    civ_data_path="civ_data.json",
                    assets_root=resource_path(""),
                    parent=self
                    )
                self.outer.addWidget(self.civ_tooltip)
                self.civ_tooltip.show()
                self.outer.addSpacing(4)
                self.footer = QLabel("Age of Duck Mod by @BubbleDuck | ELO Data by AOE2Companion")
                self.footer.setAlignment(Qt.AlignCenter)
                self.footer.setStyleSheet(f"color:{MUTED}; background:transparent;")
                self.footer.setFont(QFont("Segoe UI", max(7, self.font_size - 5), QFont.DemiBold))
                add_text_shadow(self.footer, blur=6, alpha=160)
                self.outer.addWidget(self.footer)
                self.setFixedWidth(self._s(self._BASE_WIDTH))
                self.btn_font_plus.clicked.connect(self.increase_font)
                self.btn_font_minus.clicked.connect(self.decrease_font)



                def toggle_lock(self):
                    self.locked = not self.locked
                    self.btn_lock.setText("🔒" if self.locked else "🔓")
                    for b in (self.btn_font_plus, self.btn_font_minus):
                        b.setEnabled(not self.locked)

                        def drag_bar_mousePressEvent(self, event):
                            if self.locked:
                                return
                                if event.button() == Qt.LeftButton:
                                    self.drag = True
                                    self.last_mouse_pos = event.globalPos()

                                    def drag_bar_mouseMoveEvent(self, event):
                                        if self.locked:
                                            return
                                            if self.drag:
                                                delta = event.globalPos() - self.last_mouse_pos
                                                self.move(self.x() + delta.x(), self.y() + delta.y())
                                                self.last_mouse_pos = event.globalPos()

                                                def drag_bar_mouseReleaseEvent(self, event):
                                                    if self.locked:
                                                        return
                                                        self.drag = False

                                                        def update_player_rows(self, flat_list):
                                                            for idx, widgets in enumerate(self.player_rows):
                                                                n, c, cur, pk = widgets["name_label"], widgets["civ_label"], widgets["current_label"], widgets["peak_label"]

                                                                if idx < len(flat_list):
                                                                    p = flat_list[idx]
                                                                    name = p.get("name", "")
                                                                    civ  = p.get("civ", "")
                                                                    elo  = p.get("rating")
                                                                    peak = p.get("peak")
                                                                    color = p.get("color", "#EAF2F9")
                                                                    n.setText(f'<span style="color:{color}; font-weight:bold">{name}</span>')
                                                                    c.setText(f'({civ})' if civ else "")
                                                                    cur.setText("" if elo is None else str(elo))
                                                                    pk.setText("" if peak is None else str(peak))

                                                                    n.show(); c.show(); cur.show(); pk.show()
                                                                else:
                                                                    n.clear(); c.clear(); cur.clear(); pk.clear()
                                                                    n.hide();  c.hide();  cur.hide();  pk.hide()

                                                                    self.adjustSize()

                                                                    def _force_relayout_and_redraw(self):
                                                                        if hasattr(self, "player_header_layout"):
                                                                            self.player_header_layout.invalidate()
                                                                            if hasattr(self, "player_content_layout"):
                                                                                self.player_content_layout.invalidate()
                                                                                if hasattr(self, "outer"):
                                                                                    self.outer.invalidate()
                                                                                    for w in getattr(self, "player_rows", []):
                                                                                        for key in ("name_label", "civ_label", "current_label", "peak_label"):
                                                                                            w[key].adjustSize()
                                                                                            for lbl in (getattr(self, "header_name", None),
                                                                                                getattr(self, "header_civ", None),
                                                                                                getattr(self, "header_current", None),
                                                                                                getattr(self, "header_peak", None),
                                                                                                getattr(self, "label_gamemode", None),
                                                                                                getattr(self, "label_map", None)):
                                                                                            if lbl:
                                                                                                lbl.adjustSize()
                                                                                                labels = []
                                                                                                for w in getattr(self, "player_rows", []):
                                                                                                    labels += [w["name_label"], w["civ_label"], w["current_label"], w["peak_label"]]
                                                                                                    labels += [getattr(self, "label_gamemode", None), getattr(self, "label_map", None)]
                                                                                                    for lbl in filter(None, labels):
                                                                                                        eff = lbl.graphicsEffect()
                                                                                                        if eff:
                                                                                                            eff.setEnabled(False)
                                                                                                            eff.setEnabled(True)
                                                                                                            self.adjustSize()
                                                                                                            self.updateGeometry()
                                                                                                            self.update()
                                                                                                            self.repaint()
                                                                                                            QApplication.processEvents()



                                                                                                            def increase_font(self):
                                                                                                                self.scale_factor = min(2.0, round(self.scale_factor * 1.10, 3))
                                                                                                                self.apply_scale()

                                                                                                                def decrease_font(self):
                                                                                                                    self.scale_factor = max(0.6, round(self.scale_factor / 1.10, 3))
                                                                                                                    self.apply_scale()


                                                                                                                    def _update_font_size(self):
                                                                                                                        base = max(8, int(round(DEFAULT_FONT_SIZE * self.scale_factor)))
                                                                                                                        self.label_gamemode.setFont(QFont("Segoe UI", base + 2, QFont.DemiBold))
                                                                                                                        self.label_map.setFont(QFont("Segoe UI", base + 2))
                                                                                                                        for h in (self.header_name, self.header_civ, self.header_current, self.header_peak):
                                                                                                                            h.setFont(QFont("Segoe UI", base, QFont.DemiBold))
                                                                                                                            for w in self.player_rows:
                                                                                                                                w["name_label"].setFont(QFont("Segoe UI", base, QFont.DemiBold))
                                                                                                                                for key in ("civ_label", "current_label", "peak_label"):
                                                                                                                                    w[key].setFont(QFont("Segoe UI", base))
                                                                                                                                    if hasattr(self, "footer") and self.footer is not None:
                                                                                                                                        self.footer.setFont(QFont("Segoe UI", max(7, base - 5), QFont.DemiBold))
                                                                                                                                        if hasattr(self, "civ_tooltip") and self.civ_tooltip is not None:
                                                                                                                                            try:
                                                                                                                                                self.civ_tooltip.set_font_size(base)
                                                                                                                                            except Exception:
                                                                                                                                                pass


                                                                                                                                                def apply_scale(self):
                                                                                                                                                    self.drag_bar.setFixedHeight(self._s(self._BASE_DRAG_H))
                                                                                                                                                    self.drag_bar.setFixedWidth(self._s(self._BASE_DRAG_W))
                                                                                                                                                    self.outer.setContentsMargins(*[self._s(v) for v in self._BASE_OUTER_MARGINS])
                                                                                                                                                    self.outer.setSpacing(self._s(3))
                                                                                                                                                    self.header_name.setMinimumWidth(self._s(self._BASE_HEADER_MIN[0]))
                                                                                                                                                    self.header_civ.setMinimumWidth(self._s(self._BASE_HEADER_MIN[1]))
                                                                                                                                                    self.header_current.setMinimumWidth(self._s(self._BASE_HEADER_MIN[2]))
                                                                                                                                                    self.header_peak.setMinimumWidth(self._s(self._BASE_HEADER_MIN[3]))
                                                                                                                                                    for row in self.player_rows:
                                                                                                                                                        row["layout"].setSpacing(self._s(self._BASE_ROW_SPACING))
                                                                                                                                                        if hasattr(self, "_divider") and self._divider is not None:
                                                                                                                                                            self._divider.setFixedHeight(self._s(self._BASE_DIVIDER_H))
                                                                                                                                                            self.setFixedWidth(self._s(self._BASE_WIDTH))
                                                                                                                                                            self._update_font_size()
                                                                                                                                                            base_pt = max(8, int(round(DEFAULT_FONT_SIZE * self.scale_factor)))
                                                                                                                                                            if hasattr(self, 'civ_tooltip') and self.civ_tooltip is not None:
                                                                                                                                                                self.civ_tooltip.set_scale(self.scale_factor, base_overlay_pt=base_pt)
                                                                                                                                                                self._force_relayout_and_redraw()



                                                                                                                                                                def set_loading(self, val):
                                                                                                                                                                    pass

                                                                                                                                                                    def profile_error(self, msg):
                                                                                                                                                                        self.tray_icon.showMessage("Profile Error", msg, QSystemTrayIcon.Warning)

                                                                                                                                                                        def get_civ_for_profile_id(self, match, profile_id):
                                                                                                                                                                            if not match or not profile_id:
                                                                                                                                                                                return None
                                                                                                                                                                                for team in match.get('teams', []):
                                                                                                                                                                                    for player in team.get('players', []):
                                                                                                                                                                                        if player.get('profileId') == int(profile_id):
                                                                                                                                                                                            return player.get('civName') or player.get('civ')
                                                                                                                                                                                            return None

                                                                                                                                                                                            def update_overlay(self, match, players, game_mode, map_name):
                                                                                                                                                                                                self.is_waiting = False
                                                                                                                                                                                                self.waiting_timer.stop()
                                                                                                                                                                                                self.label_gamemode.setText(f"{game_mode}")
                                                                                                                                                                                                self.label_map.setText(f"{map_name}")
                                                                                                                                                                                                team_players = {}
                                                                                                                                                                                                for p in players:
                                                                                                                                                                                                    team_players.setdefault(p["team"], []).append(p)
                                                                                                                                                                                                    flat_list = []
                                                                                                                                                                                                    all_teams = sorted(team_players.keys())
                                                                                                                                                                                                    for t in all_teams:
                                                                                                                                                                                                        flat_list += sorted(team_players[t], key=lambda x: x["name"].lower())
                                                                                                                                                                                                        self._last_flat_list = flat_list
                                                                                                                                                                                                        self.update_player_rows(flat_list)
                                                                                                                                                                                                        current_civ = self.get_civ_for_profile_id(match, self.worker.profile_id)
                                                                                                                                                                                                        if current_civ:
                                                                                                                                                                                                            print(f"Detected Profile ID civ: {current_civ}")
            self.civ_tooltip.current_profile_civ = current_civ  # You may want to define this attribute
        else:
            self.civ_tooltip.current_profile_civ = None
            prev_selected = self.civ_tooltip.combo_civs.currentText() if hasattr(self, 'civ_tooltip') else None

            civs_in_game = sorted({p["civ"] for p in players if p.get("civ")})
            sig = tuple(civs_in_game)
            if prev_selected and prev_selected not in civs_in_game and prev_selected != "Select a civ":
                civs_for_dropdown = civs_in_game + [prev_selected]
            else:
                civs_for_dropdown = civs_in_game

                if sig != self._last_civs_sig or (prev_selected and prev_selected not in civs_in_game):
                    self._last_civs_sig = sig
                    self.civ_tooltip.set_available_civs(civs_for_dropdown)


                    self.show_overlay()


                    def hide_overlay(self):
        self.is_waiting = True  # Now waiting for game again
        self._last_flat_list = []
        for player_data_widgets in self.player_rows:
            player_data_widgets["name_label"].setText("")
            player_data_widgets["civ_label"].setText("")
            player_data_widgets["current_label"].setText("")
            player_data_widgets["peak_label"].setText("")
            player_data_widgets["name_label"].hide()
            player_data_widgets["civ_label"].hide()
            player_data_widgets["current_label"].hide()
            player_data_widgets["peak_label"].hide()
            self.header_name.setVisible(False)
            self.header_civ.setVisible(False)
            self.header_current.setVisible(False)
            self.header_peak.setVisible(False)

            self.label_gamemode.setText("Waiting for game.")
            self.label_map.setText("")
            self.waiting_dot_count = 1
        self.waiting_timer.start(500)  # Update every 500ms
        if hasattr(self, 'civ_tooltip'):
            all_civs = sorted(self.civ_tooltip.civ_data.keys())
            self.civ_tooltip.set_available_civs(all_civs)
            self.civ_tooltip.reset_civ_selection()
            if getattr(self, "_aoe2_running", False):
                self.show()
            else:
                self.hide()


                def show_overlay(self):
                    if getattr(self, "_aoe2_running", False):
                        if not self.isVisible():
                            self.show()
                            self.header_name.setVisible(True)
                            self.header_civ.setVisible(True)
                            self.header_current.setVisible(True)
                            self.header_peak.setVisible(True)

                        else:
                            self.hide()

                            def animate_waiting(self):
                                dots = "." * self.waiting_dot_count
                                self.label_gamemode.setText(f"Waiting for game{dots}")
                                self.waiting_dot_count += 1
                                if self.waiting_dot_count > 3:
                                    self.waiting_dot_count = 1

                                    def main():
                                        import tempfile
                                        singleton_check = is_another_instance_running()
                                        if singleton_check is True:
                                            print("Another instance of the app is already running.")
                                            sys.exit(0)
                                            global singleton_server
                                            singleton_server = singleton_check

                                            app = QApplication(sys.argv)
                                            app.setApplicationName("Age of Duck Overlay Mod by @BubbleDuck")
                                            app.setQuitOnLastWindowClosed(False)

                                            tray_icon_path = resource_path("duck.png")
                                            tray_icon = QSystemTrayIcon(QIcon(tray_icon_path), parent=app)
                                            tray_icon.setToolTip("Age of Duck Overlay Mod by @BubbleDuck")
                                            if os.path.exists(UPDATE_FLAG_PATH):
                                                tray_icon.showMessage(
                                                    "Update complete",
                                                    "Age of Duck was updated successfully.",
                                                    QSystemTrayIcon.Information,
                                                    5000
                                                    )
                                                try:
                                                    os.remove(UPDATE_FLAG_PATH)
                                                except Exception:
                                                    pass
                                                    settings = SettingsWindow()
                                                    overlay = Overlay(tray_icon)

                                                    def best_parent():
                                                        try:
                                                            if settings.isVisible():
                                                                return settings
                                                            except Exception:
                                                                pass
                                                                return overlay

                                                                def toggle_startup():
                                                                    enabled = action_autostart.isChecked()
                                                                    set_app_startup(enabled)

                                                                    def open_donate():
                                                                        webbrowser.open("https://paypal.me/mywebdeveloper")

                                                                        def show_profile_id_help():
                                                                            webbrowser.open("https://www.aoe2insights.com")
                                                                            dlg = QDialog()
                                                                            dlg.setWindowTitle("How to find your Profile ID")
                                                                            dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint)
                                                                            layout = QVBoxLayout(dlg)
                                                                            label_text = QLabel(
                                                                                "1. Search your in-game username.<br>"
                                                                                "2. Click your profile from the list.<br>"
                                                                                "3. Your Profile ID will appear in the URL and on your profile page.<br><br>"
                                                                                "<i>Example below:</i>"
                                                                                )
                                                                            label_text.setWordWrap(True)
                                                                            label_text.setTextFormat(Qt.RichText)
                                                                            layout.addWidget(label_text)
                                                                            pix = QPixmap(resource_path("profile.png"))
                                                                            if not pix.isNull():
                                                                                label_img = QLabel()
                                                                                label_img.setPixmap(pix.scaledToWidth(350, Qt.SmoothTransformation))
                                                                                layout.addWidget(label_img)
                                                                            else:
                                                                                layout.addWidget(QLabel("(profile.png not found)"))
                                                                                dlg.setLayout(layout)
                                                                                dlg.setFixedSize(400, 380)
                                                                                dlg.raise_()
                                                                                dlg.activateWindow()
                                                                                dlg.exec_()

                                                                                def on_check_updates():
                                                                                    latest, installer_url = check_for_update()
                                                                                    parent = best_parent()
                                                                                    if latest:
                                                                                        m = QMessageBox(parent)
                                                                                        m.setIcon(QMessageBox.Question)
                                                                                        m.setWindowTitle("Update Available")
                                                                                        m.setText(f"Version {latest} is available. Install now?")
                                                                                        m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m.setWindowModality(Qt.WindowModal)            # modal to the parent
            m.setWindowFlag(Qt.WindowStaysOnTopHint, True) # sits over the (top-most) Settings
            m.raise_(); m.activateWindow()
            if m.exec_() == QMessageBox.Yes:
                download_and_run_installer(installer_url, tray_icon)
            else:
                i = QMessageBox(parent)
                i.setIcon(QMessageBox.Information)
                i.setWindowTitle("No Update")
                i.setText("You have the latest version.")
                i.setStandardButtons(QMessageBox.Ok)
                i.setWindowModality(Qt.WindowModal)
                i.setWindowFlag(Qt.WindowStaysOnTopHint, True)
                i.raise_(); i.activateWindow()
                i.exec_()


                

                def create_tray_menu():
                    menu = QMenu()
                    menu.addAction(action_settings)
        menu.addAction(action_autostart)   # only if you keep autostart (see section 5)
        menu.addAction(action_find_id)
        menu.addAction(action_donate)
        menu.addAction(action_discord)
        menu.addSeparator()
        menu.addAction(action_check_updates)
        menu.addSeparator()
        menu.addAction(action_version)
        menu.addAction(action_quit)

        if sys.platform != "win32":
            action_autostart.setEnabled(False)
            action_autostart.setVisible(False)

            tray_icon.setContextMenu(menu)


            def check_for_update_notify():
                latest, installer_url = check_for_update()
                if latest and installer_url:
                    parent = best_parent()
                    m = QMessageBox(parent)
                    m.setIcon(QMessageBox.Question)
                    m.setWindowTitle("Update Available")
                    m.setText(f"A new version ({latest}) is available.\nInstall now?")
                    m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m.setWindowModality(Qt.WindowModal)
                    m.setWindowFlag(Qt.WindowStaysOnTopHint, True)
                    m.raise_(); m.activateWindow()
                    if m.exec_() == QMessageBox.Yes:
                        download_and_run_installer(installer_url, tray_icon)



                        def apply_profile(profile_id):
                            overlay.worker.set_profile(profile_id)

                            action_settings = QAction("Settings", app)
                            action_find_id = QAction("Find my Profile ID (Game ID)", app)
                            action_autostart = QAction("Start with Windows", app)
                            action_autostart.setCheckable(True)
                            action_autostart.setChecked(is_app_startup_enabled())
                            action_donate = QAction("Donate ❤️", app)
                            action_check_updates = QAction("Check for Updates", app)
                            action_discord = QAction("Join our Discord", app)
                            action_version = QAction(f"Version: {CURRENT_VERSION}", app)
    action_version.setEnabled(False)  # Disabled, just for display
    action_quit = QAction("Quit", app)
    action_settings.triggered.connect(settings.show_and_focus)
    action_find_id.triggered.connect(show_profile_id_help)
    action_autostart.toggled.connect(toggle_startup)
    action_donate.triggered.connect(open_donate)
    action_check_updates.triggered.connect(on_check_updates)
    action_quit.triggered.connect(app.quit)
    action_discord.triggered.connect(lambda: webbrowser.open("https://discord.gg/hWsa7KS9nw"))
    create_tray_menu()
    tray_icon.show()
    tray_icon.showMessage(
        "ELO Overlay - Running",
        "Age of Duck ELO Overlay is now running.",
        QSystemTrayIcon.Information,
        5000
        )
    settings.profile_set.connect(apply_profile)
    tray_icon.activated.connect(lambda reason: settings.show_and_focus() if reason == QSystemTrayIcon.DoubleClick else None)
    initial_profile = load_last_profile_id()
    if initial_profile:
        overlay.worker.set_profile(initial_profile)
        if overlay._aoe2_running:
            overlay.show()
        else:
            settings.show_and_focus()
            QTimer.singleShot(3000, check_for_update_notify)
            update_timer = QTimer(app)
            update_timer.timeout.connect(check_for_update_notify)
            update_timer.start(21600000)

            sys.exit(app.exec_())


            if __name__ == "__main__":
                main()
