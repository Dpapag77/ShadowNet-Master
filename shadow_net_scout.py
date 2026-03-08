#!/usr/bin/env python3
"""
SHADOWNET MASTER: THE ULTIMATE BUG BOUNTY FRAMEWORK
--------------------------------------------------
A: Scout (Initial Discovery)
B: Cartographer (Permission Mapping)
C: Exploiter (Vulnerability Simulation)
D: Architect (Pattern Guessing & Multi-Cloud)
E: Whisperer (Ghost/Takeover Detection)
G: Deep Crawler (Recursive Site Exploration)
H: Bounty Hunter (Security Policy Discovery)
Z: Professional Reporter (Mission Documentation)
"""

import requests
import re
import argparse
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- CONFIGURATION ---
# Specialized User-Agent to identify our 'legal' research tool
HEADERS = {'User-Agent': 'Mozilla/5.0 (Kali Linux) ShadowNet-Research/1.1'}

# The 'DNA' patterns for the Big Three Cloud Providers
PATTERNS = {
    "AWS S3": r"([a-z0-9.-]+\.s3\.amazonaws\.com)",
    "Azure": r"([a-z0-9]+\.blob\.core\.windows\.net)",
    "Google": r"(storage\.googleapis\.com/[a-z0-9.-]+)"
}

def find_bounty_policy(domain):
    """PHASE H: The Bounty Hunter - Finding the legal reporting path."""
    print(f"[*] [H] Hunting for security disclosure policies...")
    paths = ['/.well-known/security.txt', '/security', '/security.txt', '/bug-bounty', '/responsible-disclosure']
    found_policies = []
    for path in paths:
        try:
            res = requests.get(f"https://{domain}{path}", headers=HEADERS, timeout=5)
            if res.status_code == 200:
                found_policies.append(f"https://{domain}{path}")
        except: pass
    return found_policies

def get_internal_links(base_url):
    """Part of PHASE G: Finding all hallways (links) in the mansion."""
    links = set()
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        domain = urlparse(base_url).netloc
        for a in soup.find_all('a', href=True):
            full_url = urljoin(base_url, a['href'])
            # Only stay inside the target's 'house'
            if urlparse(full_url).netloc == domain:
                links.add(full_url)
    except: pass
    return list(links)

def whisperer_check(url):
    """PHASE E: The Whisperer - Detecting Ghost assets."""
    try:
        res = requests.get(f"https://{url}", headers=HEADERS, timeout=5)
        # Check for specific provider error messages that indicate an unclaimed name
        ghost_sigs = ["NoSuchBucket", "The specified bucket does not exist", "NoSuchKey"]
        if any(sig in res.text for sig in ghost_sigs):
            return "👻 GHOST (TAKEOVER POSSIBLE)"
        elif res.status_code == 200 and ("<Contents>" in res.text or "ListBucketResult" in res.text):
            return "🔓 OPEN (CRITICAL)"
        elif res.status_code == 403:
            return "🔒 LOCKED"
        return None
    except: return None

def scan_page(url):
    """PHASE A: Scouting a single page for 'Vault' addresses."""
    found = set()
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        for provider, regex in PATTERNS.items():
            matches = re.findall(regex, res.text, re.IGNORECASE)
            for m in matches: found.add(m)
    except: pass
    return found

def architect_guess(base_name):
    """PHASE D: The Architect - Predicting hidden vaults based on patterns."""
    guesses = []
    modifiers = ['-dev', '-prod', '-staging', '-backup', '-test', '-internal', '-old']
    for mod in modifiers:
        guesses.append(f"{base_name}{mod}.s3.amazonaws.com")
        guesses.append(f"{base_name}{mod}.blob.core.windows.net")
    return guesses

def run_master_mission(domain, max_pages=10):
    print("\n" + "💎 "*25)
    print(f" SHADOWNET MASTER MISSION: {domain.upper()} ")
    print("💎 "*25)
    
    # 1. Start Bounty Hunter Policy Search
    policies = find_bounty_policy(domain)
    for p in policies: print(f"  [!] Found Policy: {p}")
    
    # 2. Deep Crawl (Phase G)
    base_url = f"https://{domain}"
    visited = set()
    to_visit = [base_url]
    discovered_assets = set()
    
    print(f"\n[*] [G] Deep crawling up to {max_pages} pages for hidden links...")
    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited: continue
        visited.add(current_url)
        
        # Discover more hallways
        new_links = get_internal_links(current_url)
        for link in new_links:
            if link not in visited: to_visit.append(link)
            
        # Scan for Vaults
        page_assets = scan_page(current_url)
        discovered_assets.update(page_assets)

    # 3. Architect Guessing (Phase D)
    print(f"[*] [D] Architect is predicting related storage names...")
    core_name = domain.split('.')[0]
    discovered_assets.update(architect_guess(core_name))

    # 4. Analyze All Findings (Phase B, C, E)
    results = []
    print(f"\n[*] [A-E] Analyzing {len(discovered_assets)} unique assets for vulnerabilities...")
    for asset in discovered_assets:
        status = whisperer_check(asset)
        if status:
            print(f"  [+] {asset} -> {status}")
            results.append(f"{asset} | {status}")

    # 5. Professional Reporting (Phase Z)
    filename = f"MASTER_REPORT_{domain}.txt"
    with open(filename, "w") as f:
        f.write(f"SHADOWNET MASTER PENETRATION REPORT\n")
        f.write(f"Target: {domain}\nDate: {datetime.now()}\n")
        f.write("="*60 + "\n\n")
        f.write("1. LEGAL RECOURSE (Security Policies Found):\n")
        if not policies: f.write("- None found. Proceed with caution.\n")
        for p in policies: f.write(f"- {p}\n")
        
        f.write("\n2. CLOUD INFRASTRUCTURE ANALYSIS:\n")
        if not results: f.write("- No critical vulnerabilities detected in sampled space.\n")
        for r in results: f.write(f"- {r}\n")
        
        f.write(f"\n3. CRAWL STATS:\n- Pages Inspected: {len(visited)}\n- Unique Assets Analyzed: {len(discovered_assets)}\n")
    
    print(f"\n[!] Mission Complete. FULL REPORT saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShadowNet Master")
    parser.add_argument("domain", help="Target domain (e.g., atlassian.com)")
    parser.add_argument("--pages", type=int, default=10, help="Max pages to deep crawl")
    args = parser.parse_args()
    run_master_mission(args.domain, args.pages)