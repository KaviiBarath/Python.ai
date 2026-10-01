import os
import time
import subprocess
import platform
import shutil
from typing import Optional

try:
    import psutil
    _PSUTIL = True
except ImportError:
    _PSUTIL = False

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
    _PYAUTOGUI = True
except ImportError:
    _PYAUTOGUI = False

_SYSTEM = platform.system()

# Comprehensive process and executable mappings
_APP_PROCESS_MAP: dict[str, dict[str, list[str]]] = {
    "chrome":             {"Windows": ["chrome.exe"],                          "Darwin": ["Google Chrome"],       "Linux": ["chrome", "google-chrome"]},
    "google chrome":      {"Windows": ["chrome.exe"],                          "Darwin": ["Google Chrome"],       "Linux": ["chrome", "google-chrome"]},
    "firefox":            {"Windows": ["firefox.exe"],                         "Darwin": ["firefox"],             "Linux": ["firefox"]},
    "edge":               {"Windows": ["msedge.exe"],                          "Darwin": ["Microsoft Edge"],      "Linux": ["msedge", "microsoft-edge"]},
    "microsoft edge":     {"Windows": ["msedge.exe"],                          "Darwin": ["Microsoft Edge"],      "Linux": ["msedge", "microsoft-edge"]},
    "brave":              {"Windows": ["brave.exe"],                           "Darwin": ["Brave Browser"],       "Linux": ["brave", "brave-browser"]},
    "opera":              {"Windows": ["opera.exe", "launcher.exe"],           "Darwin": ["Opera"],               "Linux": ["opera"]},
    "operagx":            {"Windows": ["opera.exe", "launcher.exe"],           "Darwin": ["Opera GX"],            "Linux": ["opera-gx"]},
    "safari":             {"Windows": ["msedge.exe"],                          "Darwin": ["Safari"],              "Linux": ["firefox"]},
    "whatsapp":           {"Windows": ["WhatsApp.exe", "WhatsApp.Root.exe"],    "Darwin": ["WhatsApp"],            "Linux": ["whatsapp"]},
    "telegram":           {"Windows": ["Telegram.exe"],                        "Darwin": ["Telegram"],            "Linux": ["telegram-desktop", "telegram"]},
    "discord":            {"Windows": ["Discord.exe", "DiscordCanary.exe"],    "Darwin": ["Discord"],             "Linux": ["discord"]},
    "slack":              {"Windows": ["slack.exe"],                           "Darwin": ["Slack"],               "Linux": ["slack"]},
    "zoom":               {"Windows": ["Zoom.exe"],                            "Darwin": ["zoom.us"],             "Linux": ["zoom"]},
    "teams":              {"Windows": ["ms-teams.exe", "Teams.exe"],           "Darwin": ["Microsoft Teams"],     "Linux": ["teams"]},
    "skype":              {"Windows": ["Skype.exe"],                           "Darwin": ["Skype"],               "Linux": ["skype"]},
    "spotify":            {"Windows": ["Spotify.exe"],                         "Darwin": ["Spotify"],             "Linux": ["spotify"]},
    "vlc":                {"Windows": ["vlc.exe"],                             "Darwin": ["VLC"],                 "Linux": ["vlc"]},
    "netflix":            {"Windows": ["Netflix.exe"],                         "Darwin": ["Netflix"],             "Linux": ["firefox"]},
    "vscode":             {"Windows": ["Code.exe"],                            "Darwin": ["Visual Studio Code"],  "Linux": ["code"]},
    "visual studio code": {"Windows": ["Code.exe"],                            "Darwin": ["Visual Studio Code"],  "Linux": ["code"]},
    "code":               {"Windows": ["Code.exe"],                            "Darwin": ["Visual Studio Code"],  "Linux": ["code"]},
    "terminal":           {"Windows": ["WindowsTerminal.exe", "wt.exe"],       "Darwin": ["Terminal"],            "Linux": ["x-terminal-emulator", "gnome-terminal"]},
    "cmd":                {"Windows": ["cmd.exe"],                             "Darwin": ["Terminal"],            "Linux": ["bash"]},
    "powershell":         {"Windows": ["powershell.exe", "pwsh.exe"],          "Darwin": ["Terminal"],            "Linux": ["pwsh", "bash"]},
    "notepad":            {"Windows": ["notepad.exe", "Notepad.exe"],          "Darwin": ["TextEdit"],            "Linux": ["gedit", "kate", "mousepad"]},
    "textedit":           {"Windows": ["notepad.exe"],                         "Darwin": ["TextEdit"],            "Linux": ["gedit"]},
    "word":               {"Windows": ["WINWORD.EXE", "winword.exe"],          "Darwin": ["Microsoft Word"],      "Linux": ["soffice.bin", "soffice"]},
    "excel":              {"Windows": ["EXCEL.EXE", "excel.exe"],              "Darwin": ["Microsoft Excel"],     "Linux": ["soffice.bin", "soffice"]},
    "powerpoint":         {"Windows": ["POWERPNT.EXE", "powerpnt.exe"],        "Darwin": ["Microsoft PowerPoint"],"Linux": ["soffice.bin", "soffice"]},
    "libreoffice":        {"Windows": ["soffice.bin", "soffice.exe"],          "Darwin": ["LibreOffice"],         "Linux": ["soffice.bin", "soffice"]},
    "calculator":         {"Windows": ["CalculatorApp.exe", "Calculator.exe", "calc.exe"], "Darwin": ["Calculator"], "Linux": ["gnome-calculator", "kcalc"]},
    "paint":              {"Windows": ["mspaint.exe", "PaintApp.exe"],         "Darwin": ["Preview"],             "Linux": ["gimp", "drawing"]},
    "task manager":       {"Windows": ["taskmgr.exe"],                         "Darwin": ["Activity Monitor"],    "Linux": ["gnome-system-monitor"]},
    "settings":           {"Windows": ["SystemSettings.exe"],                  "Darwin": ["System Settings"],     "Linux": ["gnome-control-center"]},
    "postman":            {"Windows": ["Postman.exe"],                         "Darwin": ["Postman"],             "Linux": ["postman"]},
    "steam":              {"Windows": ["steam.exe"],                           "Darwin": ["steam"],               "Linux": ["steam"]},
    "epic":               {"Windows": ["EpicGamesLauncher.exe"],               "Darwin": ["Epic Games Launcher"], "Linux": ["legendary"]},
}


def _get_target_process_names(app_name: str) -> list[str]:
    """Resolve user app name to possible executable process names."""
    key = app_name.lower().strip()
    
    # Exact match in aliases
    if key in _APP_PROCESS_MAP:
        return _APP_PROCESS_MAP[key].get(_SYSTEM, [key])
    
    # Partial match in aliases
    for alias_key, os_map in _APP_PROCESS_MAP.items():
        if alias_key in key or key in alias_key:
            return os_map.get(_SYSTEM, [key])
            
    # Generic fallback
    if _SYSTEM == "Windows":
        if not key.endswith(".exe"):
            return [f"{key}.exe", key]
    return [key]


def _close_notepad_windows(save_option: Optional[str] = None) -> bool:
    """Specialized handler for Notepad on Windows with save/don't save options."""
    save_opt = (save_option or "").lower().strip()

    if _PYAUTOGUI and save_opt in ("save", "yes", "dont_save", "don't save", "no", "without_saving"):
        try:
            pyautogui.FAILSAFE = False
            # Try to bring Notepad to focus
            script = '(New-Object -ComObject WScript.Shell).AppActivate("Notepad")'
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                capture_output=True, timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW if _SYSTEM == "Windows" else 0
            )
            time.sleep(0.2)
            
            if save_opt in ("save", "yes"):
                pyautogui.hotkey("ctrl", "s")
                time.sleep(0.4)
                pyautogui.hotkey("alt", "f4")
                time.sleep(0.3)
                return True
                
            elif save_opt in ("dont_save", "don't save", "no", "without_saving"):
                pyautogui.hotkey("alt", "f4")
                time.sleep(0.3)
                pyautogui.press("n")
                time.sleep(0.2)
        except Exception as e:
            print(f"[close_app] Notepad UI close failed: {e}")

    # Terminate process to guarantee it's closed
    return _kill_processes_by_names(["Notepad.exe", "notepad.exe", "notepad"], force=True)


def _kill_processes_by_names(process_names: list[str], force: bool = True) -> bool:
    """Terminate all processes matching given executable names."""
    closed_any = False
    target_names_lower = [p.lower().replace(".exe", "") for p in process_names]
    
    # Method 1: psutil (cleanest cross-platform, handles UWP/WindowsApps)
    if _PSUTIL:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pname = (proc.info['name'] or '').lower().replace(".exe", "")
                pexe = (proc.info['exe'] or '').lower()
                
                matched = False
                for t in target_names_lower:
                    if pname == t or (len(t) > 3 and t in pname) or (len(t) > 3 and t in pexe):
                        matched = True
                        break
                
                if matched:
                    try:
                        if force:
                            proc.kill()
                        else:
                            proc.terminate()
                        closed_any = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    # Method 2: Windows taskkill
    if _SYSTEM == "Windows":
        for pname in process_names:
            exe_name = pname if pname.endswith(".exe") else f"{pname}.exe"
            try:
                cmd = ["taskkill", "/IM", exe_name, "/T", "/F"]
                res = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=3,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if res.returncode == 0:
                    closed_any = True
            except Exception:
                pass

    # Method 3: macOS osascript / pkill
    elif _SYSTEM == "Darwin":
        for pname in process_names:
            try:
                subprocess.run(["pkill", "-f", pname], capture_output=True, timeout=5)
                closed_any = True
            except Exception:
                pass

    # Method 4: Linux killall / pkill
    elif _SYSTEM == "Linux":
        for pname in process_names:
            try:
                subprocess.run(["pkill", "-f", pname], capture_output=True, timeout=5)
                closed_any = True
            except Exception:
                pass

    return closed_any


def _close_active_window() -> bool:
    """Close the currently focused/active window using Alt+F4 / Cmd+W."""
    if _PYAUTOGUI:
        try:
            if _SYSTEM == "Darwin":
                pyautogui.hotkey("command", "w")
            else:
                pyautogui.hotkey("alt", "f4")
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"[close_app] Active window close failed: {e}")
    return False


def close_app(
    parameters: dict = None,
    response=None,
    player=None,
    session_memory=None,
) -> str:
    """
    Closes any application on the computer with full Windows UI & process control.
    """
    params = parameters or {}
    app_name = str(params.get("app_name", "")).strip()
    save_option = params.get("save_option", None)
    force = bool(params.get("force", True))

    if not app_name:
        return "Please specify the application to close."

    if player:
        player.write_log(f"[close_app] Closing {app_name}")

    print(f"[close_app] Request to close: '{app_name}' (save_option={save_option}, force={force})")

    app_lower = app_name.lower().strip()

    # Active / current window
    if app_lower in ("active", "current", "this window", "active window", "this app"):
        if _close_active_window():
            return "Closed current window."
        return "Could not close active window."

    # Notepad specific handling
    if "notepad" in app_lower:
        if _close_notepad_windows(save_option):
            msg = "Closed Notepad."
            if save_option in ("dont_save", "don't save", "no", "without_saving"):
                msg = "Closed Notepad without saving."
            elif save_option in ("save", "yes"):
                msg = "Saved and closed Notepad."
            return msg

    # Resolve executable names
    process_names = _get_target_process_names(app_name)
    print(f"[close_app] Target processes: {process_names}")

    success = _kill_processes_by_names(process_names, force=force)
    
    if not success:
        # Fallback: try active window close if user said close while looking at it
        if _PYAUTOGUI and ("window" in app_lower or "tab" in app_lower):
            if _close_active_window():
                return f"Closed {app_name}."

        # Also check if it's already closed
        return f"{app_name} has been closed or was not running."

    return f"Closed {app_name} successfully."


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "close_app",
    "description": (
        "Closes, terminates, quits, or exits any application or window on the computer "
        "(Chrome, Notepad, Edge, Firefox, VSCode, Spotify, Discord, WhatsApp, Telegram, "
        "Calculator, Word, Excel, VLC, Terminal, etc.). "
        "Also handles closing active window or specific apps with save/don't save options for Notepad. "
        "ALWAYS call this tool when user asks to close, quit, exit, stop, or kill an application in "
        "ANY language (English, Tamil, Tanglish: 'close pannu', 'moodu', 'terminate pannu') — NEVER simulate or just say it."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "app_name": {
                "type": "STRING",
                "description": "Name of the application to close (e.g. 'Chrome', 'Notepad', 'Spotify', 'VSCode', 'active')"
            },
            "save_option": {
                "type": "STRING",
                "description": "Optional for text editors like Notepad: 'dont_save' (close without saving) | 'save' (save and close) | 'force'"
            },
            "force": {
                "type": "BOOLEAN",
                "description": "Force kill the process if true (default: true)"
            }
        },
        "required": [
            "app_name"
        ]
    },
    "handler": close_app,
}
