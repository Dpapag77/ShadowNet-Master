# 🛰️ ShadowNet Master v2.0
### Predictive Cloud Reconnaissance & Ghost Asset Discovery

ShadowNet Master is a professional reconnaissance engine for Kali Linux. It identifies "Ghost Assets" (unclaimed cloud resources) and bypasses automated triage filters on platforms like HackerOne using Architectural Prediction logic.

---

## 🚀 Recent Mission Success: 23andMe
- **Target:** 23andMe
- **Vulnerability:** Subdomain Takeover (Dangling CNAME)
- **Status:** Reported & Open (#3593734)
- **Tool Used:** Bot-Crusher Evidence Engine

---

## 🛠️ Installation (A to Z)

Follow these steps to set up ShadowNet on your Kali Linux environment.

### 1. System Prerequisites
The GUI requires the Tkinter library and Python 3. Run this to ensure your system is ready:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk -y
2. Clone the Repository
If you are deploying this on a new machine, clone your master branch:

Bash
git clone [https://github.com/Dpapag77/ShadowNet-Master.git](https://github.com/Dpapag77/ShadowNet-Master.git)
cd ShadowNet-Master
3. Install Python Dependencies
Install the specific libraries used for cloud interrogation and HTML parsing:

Bash
pip3 install requests beautifulsoup4
🎮 How to Run
1. Launch the Cyber-Dashboard (GUI)
The recommended way to generate "Bot-Crusher" evidence logs for HackerOne.

Bash
python3 shadow_gui.py
2. Run the Stealth Scout (Terminal)
For fast reconnaissance missions directly in the command line.

Bash
python3 shadow_net_terminal.py [target.com]
📂 Project Structure
shadow_gui.py: Primary Cyber-Dashboard with live evidence generation.

shadow_net_terminal.py: Terminal-based stealth recon tool.

Reports/: Captured evidence logs and technical proof of concepts.

Disclaimer: This tool is for authorized security research and bug bounty hunting under Safe Harbor guidelines only.
