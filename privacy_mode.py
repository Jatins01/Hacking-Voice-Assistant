import subprocess
import time
import threading
import requests

def change_ip():
    try:
        adapter_name = "Wi-Fi"  
        subprocess.call(f"netsh interface set interface \"{adapter_name}\" disable", shell=True)
        time.sleep(1)
        subprocess.call(f"netsh interface set interface \"{adapter_name}\" enable", shell=True)
    except Exception as e:
        print(f"Failed to change IP: {e}")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text
    except:
        return "Unable to retrieve IP"

def start_privacy_mode():
    def ip_loop():
        while True:
            change_ip()
            ip = get_public_ip()
            print(f"[Privacy Mode] Public IP: {ip}")
            time.sleep(3)

    threading.Thread(target=ip_loop, daemon=True).start()
