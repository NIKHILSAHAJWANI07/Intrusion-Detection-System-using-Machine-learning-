import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os
import sys
import http.server
import socketserver

PORT = 8080

class IDS_GUI:
    def __init__(self, root):
        self.root = root
        root.title("🛡️ Intrusion Detection System GUI")
        root.geometry("700x500")

        tk.Label(root, text="Intrusion Detection Control Panel", font=("Arial", 16)).pack(pady=10)

        self.start_server_btn = tk.Button(root, text="▶️ Start Local Server", command=self.start_server)
        self.start_server_btn.pack(pady=5)

        self.ids_btn = tk.Button(root, text="🛡️ Start IDS Engine", command=self.toggle_ids)
        self.ids_btn.pack(pady=5)

        self.attack_frame = tk.Frame(root)
        self.attack_frame.pack(pady=10)

        # Attack buttons (row 0)
        tk.Button(self.attack_frame, text="💣 Launch DoS Attack", command=lambda: self.launch_attack("dos_attack.py")).grid(row=0, column=0, padx=5)
        tk.Button(self.attack_frame, text="💥 Launch DDoS Attack", command=lambda: self.launch_attack("ddos_attack.py")).grid(row=0, column=1, padx=5)
        tk.Button(self.attack_frame, text="🔐 Launch Ransomware Attack", command=lambda: self.launch_attack("ransomware_attack.py")).grid(row=0, column=2, padx=5)

        # Normal traffic button (row 1)
        tk.Button(self.attack_frame, text="🟢 Generate Normal Logs", command=lambda: self.launch_attack("normal_traffic.py")).grid(row=1, column=1, padx=5)

        self.log_box = scrolledtext.ScrolledText(root, width=90, height=20)
        self.log_box.pack(pady=10)

        self.log("✅ GUI Ready. Click buttons to begin.")

        self.ids_process = None  # Holds the subprocess instance

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.yview(tk.END)
        self.root.update()
        print(message)

    def start_server(self):
        class SilentHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress default HTTP log messages

        def run_server():
            logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
            os.chdir(logs_dir)
            with socketserver.TCPServer(("", PORT), SilentHandler) as httpd:
                self.log(f"🌐 Server running at http://localhost:{PORT}/")
                httpd.serve_forever()

        threading.Thread(target=run_server, daemon=True).start()

    def toggle_ids(self):
        if self.ids_process is None:
            self.ids_btn.config(text="🛑 Stop IDS Engine")
            self.log("🛡️ Starting IDS engine...")

            def run_ids():
                base_dir = os.path.dirname(os.path.abspath(__file__))
                path_to_ids = os.path.join(base_dir, "ids_engine.py")

                if not os.path.isfile(path_to_ids):
                    self.log(f"❌ IDS engine script not found at {path_to_ids}")
                    self.ids_process = None
                    self.ids_btn.config(text="🛡️ Start IDS Engine")
                    return

                self.ids_process = subprocess.Popen(
                    [sys.executable, path_to_ids],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=base_dir
                )

                for line in self.ids_process.stdout:
                    self.log(line.strip())

                self.ids_process = None
                self.log("🛡️ IDS engine stopped.")
                self.ids_btn.config(text="🛡️ Start IDS Engine")

            threading.Thread(target=run_ids, daemon=True).start()

        else:
            self.log("🛡️ Stopping IDS engine...")
            if self.ids_process:
                if os.name == 'nt':
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.ids_process.pid)])
                else:
                    self.ids_process.terminate()
                self.ids_process = None
            self.ids_btn.config(text="🛡️ Start IDS Engine")

    def launch_attack(self, script):
        self.log(f"⚠️ Launching {script}...")

        def run():
            base_dir = os.path.dirname(os.path.abspath(__file__))
            attack_path = os.path.join(base_dir, "attack_tools", script)

            if not os.path.isfile(attack_path):
                self.log(f"❌ Attack script not found: {attack_path}")
                return

            proc = subprocess.Popen(
                [sys.executable, attack_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, universal_newlines=True,
                cwd=base_dir
            )

            for line in proc.stdout:
                self.log(line.strip())
            proc.wait()
            self.log(f"⚠️ {script} finished.")

        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = IDS_GUI(root)
    root.mainloop()
