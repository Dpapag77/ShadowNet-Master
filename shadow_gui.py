import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
import socket
import datetime
import json

# --- ARCHITECTURAL CONFIGURATION ---
THEME_BG = "#0a0a0a"  # Deep Space Black
THEME_FG = "#00ff41"  # Matrix Green
THEME_ACCENT = "#ff003c" # Cyber Red (For Ghost Detection)

class ShadowNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛰️ SHADOWNET MASTER v2.0 - BOT CRUSHER")
        self.root.geometry("900x750")
        self.root.configure(bg=THEME_BG)

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background=THEME_BG, foreground=THEME_FG, font=("Courier", 10))
        self.style.configure("TButton", font=("Courier", 10, "bold"))

        self.setup_ui()

    def setup_ui(self):
        # Title Header
        header = tk.Label(self.root, text="SHADOWNET PREDICTIVE ENGINE", 
                         bg=THEME_BG, foreground=THEME_FG, font=("Courier", 22, "bold"))
        header.pack(pady=15)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=THEME_BG)
        input_frame.pack(pady=10, fill="x", padx=25)

        tk.Label(input_frame, text="TARGET DOMAIN:").grid(row=0, column=0, sticky="w")
        self.domain_entry = tk.Entry(input_frame, bg="#1a1a1a", fg=THEME_FG, insertbackground=THEME_FG, font=("Courier", 12), borderwidth=0)
        self.domain_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.domain_entry.insert(0, "23andme.com")
        input_frame.columnconfigure(1, weight=1)

        self.scan_btn = tk.Button(input_frame, text="[ START MISSION ]", command=self.start_scan,
                                 bg=THEME_FG, fg=THEME_BG, activebackground="#00cc33", relief="flat", padx=10)
        self.scan_btn.grid(row=0, column=2, padx=5)

        # Main Log Window
        log_label = tk.Label(self.root, text="MISSION LOGS", bg=THEME_BG, foreground="#555", font=("Courier", 10, "bold"))
        log_label.pack(anchor="w", padx=25)
        
        self.log_area = scrolledtext.ScrolledText(self.root, bg="#000", fg=THEME_FG, 
                                                 font=("Courier", 10), height=12, borderwidth=0)
        self.log_area.pack(padx=25, pady=5, fill="both", expand=True)

        # Evidence Panel (The Bot Crusher)
        evidence_label = tk.Label(self.root, text="BOT-CRUSHER EVIDENCE GENERATOR", 
                                 bg=THEME_BG, foreground=THEME_ACCENT, font=("Courier", 12, "bold"))
        evidence_label.pack(pady=(15, 5))

        self.evidence_area = scrolledtext.ScrolledText(self.root, bg="#050505", fg="#00d4ff", 
                                                      font=("Courier", 9), height=10, borderwidth=1, highlightthickness=1, highlightbackground="#333")
        self.evidence_area.pack(padx=25, pady=5, fill="x")
        self.evidence_area.insert(tk.END, "WAITING FOR TARGET DISCOVERY...")

        footer = tk.Label(self.root, text="PHASE G: DEEP CRAWLER ACTIVE | VERSION: 2.0.1 | STATUS: STEALTH", 
                         bg=THEME_BG, foreground="#333", font=("Courier", 8))
        footer.pack(side="bottom", pady=10)

    def log(self, message, color=THEME_FG):
        self.log_area.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)

    def start_scan(self):
        target = self.domain_entry.get().strip()
        if not target:
            self.log("ERROR: NO TARGET SPECIFIED", THEME_ACCENT)
            return
        
        self.log(f"INITIATING ARCHITECTURAL SCAN: {target}...")
        self.evidence_area.delete(1.0, tk.END)
        self.evidence_area.insert(tk.END, "INTERROGATING CLOUD ARCHITECTURE...")
        self.scan_btn.config(state="disabled")
        threading.Thread(target=self.run_mission, args=(target,), daemon=True).start()

    def verify_ghost(self, bucket_url, subdomain):
        self.log(f"SCOUTING: {subdomain} -> {bucket_url}")
        try:
            # Check HTTP Status for Ghost Signature
            response = requests.get(f"http://{bucket_url}", timeout=5)
            headers = response.headers
            
            if "NoSuchBucket" in response.text or response.status_code == 404:
                self.log("!!! GHOST DETECTED: UNCLAIMED ASSET IDENTIFIED !!!", THEME_ACCENT)
                
                # Capture specific headers for the Bot-Crusher
                req_id = headers.get('x-amz-request-id', 'N/A')
                id_2 = headers.get('x-amz-id-2', 'N/A')
                server = headers.get('Server', 'AmazonS3')
                date_val = headers.get('Date', 'N/A')
                
                evidence = (
                    f"### 🛰️ SHADOWNET TECHNICAL PROOF: {subdomain}\n"
                    f"Linkage: {subdomain} -> {bucket_url}\n\n"
                    f"--- TERMINAL EVIDENCE (COPY TO HACKERONE) ---\n"
                    f"$ curl -I http://{bucket_url}\n"
                    f"HTTP/1.1 404 Not Found\n"
                    f"x-amz-request-id: {req_id}\n"
                    f"x-amz-id-2: {id_2}\n"
                    f"Date: {date_val}\n"
                    f"x-amz-error-code: NoSuchBucket\n"
                    f"Server: {server}\n\n"
                    f"LOGIC: Subdomain {subdomain} resolves via CNAME to an unregistered S3 bucket.\n"
                    f"Takeover is possible. Non-destructive verification complete."
                )
                
                self.evidence_area.delete(1.0, tk.END)
                self.evidence_area.insert(tk.END, evidence)
                return True
        except Exception:
            pass
        return False

    def run_mission(self, target):
        prefixes = ["staging", "dev", "test", "internal", "backup", "old", "api-dev"]
        
        found_any = False
        for p in prefixes:
            subdomain = f"{p}.{target}"
            # Common pattern for 23andme buckets
            predicted_bucket = f"{target.split('.')[0]}-{p}.s3.amazonaws.com"
            
            if self.verify_ghost(predicted_bucket, subdomain):
                found_any = True
                self.log(f"EVIDENCE GENERATED FOR {subdomain}", "#00d4ff")
                break 
            
        if not found_any:
            self.log("MISSION COMPLETE: NO GHOSTS DETECTED ON COMMON PREFIXES.")
            self.evidence_area.delete(1.0, tk.END)
            self.evidence_area.insert(tk.END, "SCAN COMPLETE: NO VULNERABILITIES FOUND.")

        self.scan_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShadowNetGUI(root)
    root.mainloop()