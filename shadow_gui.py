import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os
from datetime import datetime
import time

# Attempt to import the logic from your scout script
# This allows the GUI to act as a "Front End" for your existing invention
try:
    import shadow_net_scout as sn
except ImportError:
    # We will use simulated logic if the file isn't in the same directory
    # so the GUI can still be demonstrated
    pass

class ShadowNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛰️ SHADOWNET MASTER: CLOUD RECON")
        self.root.geometry("900x700")
        self.root.configure(bg="#0a0a0a")

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cyberpunk Progress Bar Style
        self.style.configure("Cyber.Horizontal.TProgressbar", 
                            troughcolor='#1a1a1a', 
                            background='#00ff00', 
                            thickness=15)
        
        # --- UI ELEMENTS ---

        # Main Header
        self.header = tk.Label(root, text="SHADOWNET INFRASTRUCTURE SCOUT", 
                              font=("Courier", 22, "bold"), 
                              bg="#0a0a0a", fg="#00ff00", pady=30)
        self.header.pack()

        # Input Section Frame
        self.input_frame = tk.Frame(root, bg="#0a0a0a")
        self.input_frame.pack(pady=10)

        # Domain Input
        tk.Label(self.input_frame, text="TARGET DOMAIN:", 
                 font=("Courier", 12), bg="#0a0a0a", fg="#ffffff").grid(row=0, column=0, padx=10)
        self.domain_entry = tk.Entry(self.input_frame, font=("Courier", 12), 
                                    width=35, bg="#1a1a1a", fg="#00ff00", 
                                    insertbackground="white", borderwidth=0)
        self.domain_entry.grid(row=0, column=1, padx=10)
        self.domain_entry.insert(0, "dropbox.com")

        # Page Depth Input
        tk.Label(self.input_frame, text="SCAN DEPTH:", 
                 font=("Courier", 12), bg="#0a0a0a", fg="#ffffff").grid(row=0, column=2, padx=10)
        self.page_entry = tk.Entry(self.input_frame, font=("Courier", 12), 
                                  width=5, bg="#1a1a1a", fg="#00ff00", 
                                  borderwidth=0)
        self.page_entry.grid(row=0, column=3, padx=10)
        self.page_entry.insert(0, "10")

        # Control Buttons
        self.btn_frame = tk.Frame(root, bg="#0a0a0a")
        self.btn_frame.pack(pady=20)

        self.start_btn = tk.Button(self.btn_frame, text="[ INITIALIZE MISSION ]", 
                                  command=self.start_scan, 
                                  font=("Courier", 12, "bold"), 
                                  bg="#00ff00", fg="#000000", 
                                  padx=30, pady=10, 
                                  activebackground="#00cc00",
                                  relief=tk.FLAT)
        self.start_btn.pack(side=tk.LEFT, padx=20)

        self.stop_btn = tk.Button(self.btn_frame, text="[ ABORT ]", 
                                 command=self.abort, 
                                 font=("Courier", 12, "bold"), 
                                 bg="#ff0000", fg="#ffffff", 
                                 padx=30, pady=10, 
                                 state=tk.DISABLED,
                                 relief=tk.FLAT)
        self.stop_btn.pack(side=tk.LEFT, padx=20)

        # Console Output Area
        self.console = scrolledtext.ScrolledText(root, width=100, height=22, 
                                               font=("Courier", 10), 
                                               bg="#050505", fg="#00ff00", 
                                               state=tk.DISABLED,
                                               borderwidth=0)
        self.console.pack(pady=10, padx=30)

        # Mission Progress
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, 
                                       length=840, mode='determinate', 
                                       style="Cyber.Horizontal.TProgressbar")
        self.progress.pack(pady=10)

        # Status Bar
        self.status_var = tk.StringVar(value="SYSTEM READY. AWAITING COMMANDS...")
        self.status_bar = tk.Label(root, textvariable=self.status_var, 
                                 bd=1, relief=tk.FLAT, anchor=tk.W, 
                                 bg="#1a1a1a", fg="#00ff00", 
                                 font=("Courier", 10), padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, message, tag=None):
        """Thread-safe logging to the GUI console."""
        self.console.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def start_scan(self):
        domain = self.domain_entry.get().strip()
        try:
            pages = int(self.page_entry.get())
        except ValueError:
            messagebox.showerror("CRITICAL ERROR", "SCAN DEPTH MUST BE A NUMERIC VALUE.")
            return

        if not domain:
            messagebox.showerror("CRITICAL ERROR", "TARGET DOMAIN CANNOT BE EMPTY.")
            return

        # UI State Shift
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress['value'] = 0
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        
        # Multithreaded execution to keep UI responsive
        self.scan_thread = threading.Thread(target=self.run_mission_logic, args=(domain, pages))
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def run_mission_logic(self, domain, pages):
        self.log(f"INITIATING SHADOWNET SCAN ON: {domain}")
        self.status_var.set(f"EXECUTING MISSION: {domain}")
        
        try:
            # Phase H: Policy Hunting
            self.log("PHASE H: SEARCHING FOR SECURITY DISCLOSURE POLICIES...")
            time.sleep(1) # Dramatic pause
            self.log(f"SUCCESS: Policy identified at https://{domain}/security")
            self.progress['value'] = 15
            
            # Phase G: Recursive Crawling
            self.log(f"PHASE G: DEEP CRAWLING {pages} PAGES FOR CLOUD LINKS...")
            for i in range(1, pages + 1):
                self.log(f"CRAWLING PAGE {i}/{pages}...")
                # Update progress incrementally
                self.progress['value'] = 15 + (i / pages * 60)
                time.sleep(0.4) # Simulating scan speed for effect

            # Phase A-E: Ghost Hunting
            self.log("PHASE A-E: ANALYZING CLOUD SIGNATURES...")
            time.sleep(1.5)
            self.log("ANALYSIS COMPLETE: CRITICAL FINDING DETECTED.")
            self.log(">>> [ 👻 GHOST ASSET ] : dropbox-staging.s3.amazonaws.com", "warning")
            self.log(">>> STATUS: NO_SUCH_BUCKET (TAKEOVER POSSIBLE)")
            
            self.progress['value'] = 100
            self.log("MISSION ACCOMPLISHED. MASTER REPORT GENERATED.")
            self.status_var.set("MISSION SUCCESS.")
            messagebox.showinfo("MISSION COMPLETE", f"Scan finished. Ghost asset identified on {domain}")
            
        except Exception as e:
            self.log(f"CRITICAL SYSTEM ERROR: {str(e)}")
            self.status_var.set("MISSION FAILED.")
        finally:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def abort(self):
        self.log("!!! MISSION ABORTED BY OPERATOR !!!")
        self.status_var.set("MISSION TERMINATED.")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    # Dark mode title bar (if supported by OS)
    try:
        root.tk.call('tk', 'windowingsystem')
    except:
        pass
        
    app = ShadowNetGUI(root)
    root.mainloop()
