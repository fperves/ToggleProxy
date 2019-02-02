from infi.systray import SysTrayIcon
import subprocess
import winreg
import webbrowser
import os

proxy_activated = "ToggleProxy : Proxy Activated"
proxy_deactivated = "ToggleProxy : Proxy Deactivated"
script_dir = os.path.dirname(os.path.realpath(__file__))
img_dir = os.path.join(script_dir, "img")
activated_icon = os.path.join(img_dir,"activated.ico")
deactivated_icon = os.path.join(img_dir,"deactivated.ico")
hover_text = "ToggleProxy"

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
REG_KEY_PROXY = "ProxyEnable"
REG_KEY_AUTOCONFIG = "AutoConfigURL"
REG_KEY_OLDAUTOCONFIG = "OldAutoConfigURL"
SWITCH_PROXY_URL = "https://github.com/fperves/ToggleProxy"

def set_reg(name, value, type):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, type, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def del_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
        res=winreg.DeleteValue(registry_key, name)
        winreg.CloseKey(registry_key)
        return None
    except WindowsError:
        return None


def read_current_config():
    result = get_reg(REG_KEY_PROXY)

    if result == 0:
        result = proxy_deactivated
        status_icon = deactivated_icon
    if result == 1:
        result = proxy_activated
        status_icon = activated_icon

    sysTrayIcon.update(icon=status_icon, hover_text=result)
    return result

def about(sysTrayIcon):
    webbrowser.open(SWITCH_PROXY_URL, new=2, autoraise=True)
    return

def open_proxy_settings(sysTrayIcon):
    try:
        subprocess.check_output("control inetcpl.cpl, , 4")
    except:
        pass

def activate_proxy(sysTrayIcon):
    try:
        if (read_current_config() == proxy_deactivated):
            result = set_reg(REG_KEY_PROXY, 0x00000001, winreg.REG_DWORD)
            result = get_reg(REG_KEY_OLDAUTOCONFIG)
            result = set_reg(REG_KEY_AUTOCONFIG, result, winreg.REG_SZ)
            result = del_reg(REG_KEY_OLDAUTOCONFIG)
            read_current_config()
    except:
        pass

def deactivate_proxy(sysTrayIcon):
    try:
        if (read_current_config() == proxy_activated):
            result = set_reg(REG_KEY_PROXY, 0x00000000, winreg.REG_DWORD)
            result = get_reg(REG_KEY_AUTOCONFIG)
            result = set_reg(REG_KEY_OLDAUTOCONFIG, result, winreg.REG_SZ)
            result = del_reg(REG_KEY_AUTOCONFIG)
            read_current_config()
    except:
        pass

def bye(sysTrayIcon):
    pass

menu_options = (('Open Proxy Settings', "hello.ico", open_proxy_settings),
                ('Activate Proxy', None, activate_proxy),
                ('Deactivate Proxy', None, deactivate_proxy),
                ('About', None, about),
               )

sysTrayIcon = SysTrayIcon(None, hover_text, menu_options, on_quit=bye, default_menu_index=1)
current_status=read_current_config()

sysTrayIcon.start()