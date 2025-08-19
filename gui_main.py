import threading
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext

from voice import speak, takeCommand, wishMe
from phishing_detector import check_url_phishing
from wifi_audit import scan_wifi_networks
from port_scanner import run_nmap_scan
from privacy_mode import start_privacy_mode
from gemini_ai import ask_ai
from arp_spoof_detector import start_arp_spoof_detector
from metadata_cleaner import remove_metadata

# ---------------- UI Helpers ----------------
def set_output(text_widget, text):
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text if text else "")
    text_widget.config(state="disabled")
    text_widget.see(tk.END)

def prompt_text(title, prompt):
    return simpledialog.askstring(title, prompt)

# ---------------- Core Command Router ----------------
def handle_command(query, output_text, root_ref):
    q = (query or "").lower().replace("-", "").strip()
    result = ""

    if 'fishing link' in q or 'check url' in q:
        url = prompt_text("Phishing Check", "Enter URL to check:")
        if url:
            result = check_url_phishing(url)

    elif 'scan wifi' in q or 'wifi audit' in q:
        speak("Scanning nearby Wi-Fi networks...")
        data = scan_wifi_networks()
        result = str(data) if data else "No networks found or scan failed."
        speak("Scan complete. Check results.")

    elif 'scan for exploits' in q or 'port scan' in q:
        ip = prompt_text("Port Scan", "Enter target IP:")
        if ip:
            speak("Scanning open ports with Nmap...")
            ports_services = run_nmap_scan(ip)
            if not ports_services:
                result = "No open ports found or scan failed."
            else:
                lines = [f"Port {p}: {s}" for p, s in ports_services.items()]
                result = "\n".join(lines)
                speak(f"Found {len(ports_services)} open ports.")

    elif 'privacy mode' in q:
        start_privacy_mode()
        result = "Privacy mode activated for 10 minutes."

    elif 'arp detect' in q:
        threading.Thread(target=start_arp_spoof_detector, daemon=True).start()
        result = "ARP spoof detection started."

    elif 'clean metadata' in q:
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp *.tiff *.bmp"), ("All files", "*.*")]
        )
        if path:
            try:
                remove_metadata(path)
                result = f"Metadata cleaned for: {path}"
            except Exception as e:
                result = f"Failed to clean metadata: {e}"

    elif 'exit' in q or 'stop' in q:
        speak("Goodbye! Have a nice day.")
        try:
            root_ref.quit()
        except:
            pass
        return

    else:
        # ✅ Gemini fallback
        result = ask_ai(q)

    if result:
        set_output(output_text, result)
        speak(result)

# ---------------- Voice Button Action ----------------
def on_voice_button(output_text, voice_btn, root_ref):
    def worker():
        try:
            voice_btn.config(state="disabled", text="🎧 Listening…")
            speak("Listening for your command.")
            query = takeCommand()
            if not query:
                messagebox.showinfo("Voice", "Sorry, I didn't catch that.")
                return
            set_output(output_text, f"You said: {query}")
            handle_command(query, output_text, root_ref)
        finally:
            voice_btn.config(state="normal", text="🎤 Voice Command")
    threading.Thread(target=worker, daemon=True).start()

# ---------------- Optional: Direct Ask AI button ----------------
def on_ask_ai(output_text):
    q = prompt_text("Ask HackSpeak (Gemini)", "Type your question:")
    if not q:
        return
    def worker():
        resp = ask_ai(q)
        set_output(output_text, resp)
        speak(resp)
    threading.Thread(target=worker, daemon=True).start()

# ---------------- GUI ----------------
def run_gui():
    root = tk.Tk()
    root.title("HackSpeak Assistant")
    root.geometry("1200x700")  # Bigger so everything fits
    root.configure(bg="#121212")

    title = tk.Label(root, text="HackSpeak Assistant",
                     font=("Segoe UI", 24, "bold"),
                     fg="white", bg="#121212")
    title.pack(pady=15)

    # Result panel (clean, not a terminal)
    output_label = tk.Label(root,
                            text="Welcome! Use buttons or tap 🎤 and speak like before.",
                            font=("Segoe UI", 14),
                            wraplength=1100,
                            fg="white", bg="#1e1e1e",
                            justify="left", anchor="nw",
                            padx=14, pady=14)
    output_label.pack(pady=20, fill="both", expand=True)

    # Button rows
    row1 = tk.Frame(root, bg="#121212")
    row2 = tk.Frame(root, bg="#121212")
    row1.pack(pady=8)
    row2.pack(pady=8)

    def add_btn(parent, text, cmd, color="#03dac6", fg="black"):
        btn = tk.Button(parent, text=text, width=18, height=3,
                        command=cmd, bg=color, fg=fg,
                        font=("Segoe UI", 11, "bold"))
        btn.pack(side="left", padx=12, pady=8)
        return btn

    # Feature buttons (row1)
    add_btn(row1, "Check URL",   lambda: handle_command("check url", output_label, root))
    add_btn(row1, "Wi-Fi Audit", lambda: handle_command("scan wifi", output_label, root))
    add_btn(row1, "Port Scan",   lambda: handle_command("port scan", output_label, root))
    add_btn(row1, "Privacy Mode",lambda: handle_command("privacy mode", output_label, root))

    # Feature buttons (row2)
    add_btn(row2, "ARP Detect",  lambda: handle_command("arp detect", output_label, root))
    add_btn(row2, "Clean Metadata", lambda: handle_command("clean metadata", output_label, root))
    add_btn(row2, "Ask AI (Gemini)", lambda: on_ask_ai(output_label),
            color="#7c4dff", fg="white")

    # 🎤 Voice button (must be defined after)
    def voice_cmd():
        on_voice_button(output_label, btn_voice, root)

    btn_voice = add_btn(row2, "🎤 Voice Command",
                        voice_cmd,
                        color="#ff0266", fg="white")

    wishMe()
    speak("Assistant ready. Tap the voice button and speak commands like before.")
    root.mainloop()


if __name__ == "__main__":
    run_gui()
