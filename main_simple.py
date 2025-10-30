#!/usr/bin/env python3
"""
Agentic AI Security System - Simple Demo Version
Multiple autonomous agents working together to detect threats.
"""

import os
import time
import hashlib
from datetime import datetime


# ============================================================================
# MALWARE DATABASE
# ============================================================================

KNOWN_MALWARE = {
    # EICAR test file (safe test malware)
    '275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f': 'EICAR-Test-File',
}

SUSPICIOUS_EXTENSIONS = [
    '.exe', '.vbs', '.bat', '.scr', '.cmd', '.com',
    '.pif', '.application', '.msi', '.jar', '.sh', '.ps1'
]

SUSPICIOUS_KEYWORDS = [
    'virus', 'malware', 'trojan', 'worm', 'ransomware',
    'crack', 'keygen', 'hack', 'cheat', 'password',
    'stealer', 'logger', 'backdoor', 'rootkit', 'miner'
]


# ============================================================================
# AGENT 1: FILE WATCHER
# ============================================================================

class FileWatcherAgent:
    """Autonomous agent that monitors file system for new files."""

    def __init__(self, watch_path):
        self.name = "FileWatcher"
        self.watch_path = watch_path
        self.seen_files = set()
        print(f"[{self.name}] Agent initialized - Monitoring: {watch_path}")

    def check_for_new_files(self):
        """Perceive environment - detect new files."""
        try:
            current_files = set(os.listdir(self.watch_path))
        except Exception as e:
            return []

        new_files = current_files - self.seen_files
        self.seen_files = current_files

        detected = []
        for filename in new_files:
            filepath = os.path.join(self.watch_path, filename)

            # Skip directories and hidden files
            if not os.path.isfile(filepath) or filename.startswith('.'):
                continue

            # Agent's decision: Should this file be reported?
            priority = self.calculate_priority(filename, filepath)

            print(f"\n{'='*70}")
            print(f"[{self.name}] NEW FILE DETECTED")
            print(f"  File: {filename}")
            print(f"  Location: {filepath}")
            print(f"  Initial Priority: {priority}/100")
            print(f"  Reasoning: Suspicious patterns detected" if priority > 30 else "  Reasoning: Routine file download")

            detected.append({
                'filename': filename,
                'filepath': filepath,
                'priority': priority
            })

        return detected

    def calculate_priority(self, filename, filepath):
        """Agent reasoning: Calculate how suspicious this file is."""
        priority = 0
        extension = os.path.splitext(filename)[1].lower()

        # Suspicious extension?
        if extension in SUSPICIOUS_EXTENSIONS:
            priority += 40

        # Suspicious keywords in name?
        filename_lower = filename.lower()
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in filename_lower:
                priority += 30
                break

        # Double extension trick?
        if filename.count('.') > 1:
            priority += 25

        return min(priority, 100)


# ============================================================================
# AGENT 2: MALWARE SCANNER
# ============================================================================

class ScannerAgent:
    """Autonomous agent that analyzes files for threats."""

    def __init__(self):
        self.name = "Scanner"
        print(f"[{self.name}] Agent initialized - Ready to analyze files")

    def analyze_file(self, file_info):
        """Analyze a file and return threat assessment."""
        filepath = file_info['filepath']
        filename = file_info['filename']

        print(f"\n[{self.name}] ANALYZING FILE")
        print(f"  Target: {filename}")

        threat_score = 0
        reasons = []

        # Check 1: File hash against known malware
        try:
            file_hash = self.get_file_hash(filepath)
            print(f"  File hash: {file_hash[:32]}...")

            if file_hash in KNOWN_MALWARE:
                threat_score = 100
                reasons.append(f"Known malware: {KNOWN_MALWARE[file_hash]}")
                print(f"  ⚠️  MATCH: Known malware signature detected!")
        except Exception as e:
            print(f"  Warning: Could not hash file - {e}")

        # Check 2: Extension analysis
        extension = os.path.splitext(filename)[1].lower()
        if extension in SUSPICIOUS_EXTENSIONS:
            ext_score = 40
            threat_score += ext_score
            reasons.append(f"High-risk extension: {extension} (+{ext_score})")
            print(f"  🔴 High-risk extension: {extension}")

        # Check 3: Filename keywords
        filename_lower = filename.lower()
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in filename_lower:
                kw_score = 30
                threat_score += kw_score
                reasons.append(f"Suspicious keyword: '{keyword}' (+{kw_score})")
                print(f"  🔴 Suspicious keyword found: '{keyword}'")
                break

        # Check 4: Double extension trick
        if filename.count('.') > 1:
            double_score = 25
            threat_score += double_score
            reasons.append(f"Double extension detected (+{double_score})")
            print(f"  🔴 Double extension trick detected")

        # Check 5: File size anomaly
        try:
            size = os.path.getsize(filepath)
            if size < 1024:
                size_score = 15
                threat_score += size_score
                reasons.append(f"Suspiciously small file: {size} bytes (+{size_score})")
                print(f"  ⚠️  Very small file: {size} bytes")
        except:
            pass

        threat_score = min(threat_score, 100)

        print(f"\n[{self.name}] ANALYSIS COMPLETE")
        print(f"  Final Threat Score: {threat_score}/100")
        if reasons:
            print(f"  Reasons:")
            for reason in reasons:
                print(f"    • {reason}")
        else:
            print(f"  Reasons: No threats detected - file appears safe")

        return {
            'threat_score': threat_score,
            'reasons': reasons,
            'filename': filename,
            'filepath': filepath
        }

    def get_file_hash(self, filepath):
        """Calculate SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


# ============================================================================
# AGENT 3: COORDINATOR
# ============================================================================

class CoordinatorAgent:
    """Central intelligence - makes decisions based on all agent reports."""

    def __init__(self):
        self.name = "Coordinator"
        print(f"[{self.name}] Agent initialized - Central decision-making system")

    def make_decision(self, analysis_result):
        """Decide action based on threat score."""
        threat_score = analysis_result['threat_score']
        filename = analysis_result['filename']

        print(f"\n[{self.name}] MAKING DECISION")
        print(f"  Input: Threat score = {threat_score}/100")

        # Agent's decision-making logic
        if threat_score >= 90:
            decision = 'QUARANTINE_IMMEDIATELY'
            urgency = 'CRITICAL'
            print(f"  Reasoning: Score ≥ 90 indicates known malware")
        elif threat_score >= 70:
            decision = 'QUARANTINE_AND_ALERT'
            urgency = 'HIGH'
            print(f"  Reasoning: Score ≥ 70 indicates high-risk threat")
        elif threat_score >= 50:
            decision = 'ALERT_USER'
            urgency = 'MEDIUM'
            print(f"  Reasoning: Score ≥ 50 indicates suspicious file")
        elif threat_score >= 30:
            decision = 'LOG_ONLY'
            urgency = 'LOW'
            print(f"  Reasoning: Score ≥ 30 indicates minor concerns")
        else:
            decision = 'SAFE'
            urgency = 'NONE'
            print(f"  Reasoning: Score < 30 indicates file appears safe")

        print(f"  Decision: {decision}")
        print(f"  Urgency Level: {urgency}")

        return {
            'decision': decision,
            'urgency': urgency,
            'threat_score': threat_score,
            'filename': filename
        }


# ============================================================================
# AGENT 4: ALERT & RESPONSE
# ============================================================================

class AlertAgent:
    """Agent responsible for notifying user and taking action."""

    def __init__(self):
        self.name = "Alert"
        self.alerts_sent = 0
        print(f"[{self.name}] Agent initialized - Notification system ready")

    def execute_response(self, decision_result):
        """Take appropriate action based on coordinator's decision."""
        decision = decision_result['decision']
        urgency = decision_result['urgency']
        filename = decision_result['filename']
        threat_score = decision_result['threat_score']

        print(f"\n[{self.name}] EXECUTING RESPONSE")

        if decision == 'QUARANTINE_IMMEDIATELY' or decision == 'QUARANTINE_AND_ALERT':
            print(f"  🚨 CRITICAL ALERT 🚨")
            print(f"  Threat Level: {urgency}")
            print(f"  File: {filename}")
            print(f"  Score: {threat_score}/100")
            print(f"  Action: File would be QUARANTINED")
            print(f"  Notification: Desktop alert would appear")
            print(f"  Sound: Warning alarm would play")
            self.alerts_sent += 1

        elif decision == 'ALERT_USER':
            print(f"  ⚠️  WARNING")
            print(f"  Threat Level: {urgency}")
            print(f"  File: {filename}")
            print(f"  Score: {threat_score}/100")
            print(f"  Action: User notification sent")
            print(f"  Recommendation: Manual review suggested")
            self.alerts_sent += 1

        elif decision == 'LOG_ONLY':
            print(f"  ℹ️  LOGGED")
            print(f"  File: {filename}")
            print(f"  Score: {threat_score}/100")
            print(f"  Action: Logged for monitoring")

        else:  # SAFE
            print(f"  ✅ FILE SAFE")
            print(f"  File: {filename}")
            print(f"  Score: {threat_score}/100")
            print(f"  Action: No action needed")

        print(f"  Total alerts sent: {self.alerts_sent}")


# ============================================================================
# MAIN SYSTEM
# ============================================================================

class AgenticSecuritySystem:
    """Main system that coordinates all agents."""

    def __init__(self, watch_path):
        print("\n" + "="*70)
        print("  AGENTIC AI SECURITY MONITORING SYSTEM")
        print("  Multi-Agent Threat Detection & Response")
        print("="*70)

        # Initialize all agents
        self.file_watcher = FileWatcherAgent(watch_path)
        self.scanner = ScannerAgent()
        self.coordinator = CoordinatorAgent()
        self.alert = AlertAgent()

        print(f"\n✓ All agents initialized and active")
        print(f"✓ Monitoring: {watch_path}")
        print(f"\n{'='*70}")
        print("System is now monitoring for threats...")
        print("Drop files into the monitored folder to test detection")
        print(f"{'='*70}\n")

    def run(self):
        """Main monitoring loop."""
        try:
            while True:
                # Agent 1: File Watcher perceives environment
                new_files = self.file_watcher.check_for_new_files()

                for file_info in new_files:
                    # Agent 2: Scanner analyzes the file
                    analysis = self.scanner.analyze_file(file_info)

                    # Agent 3: Coordinator makes decision
                    decision = self.coordinator.make_decision(analysis)

                    # Agent 4: Alert executes response
                    self.alert.execute_response(decision)

                    print(f"\n{'='*70}\n")

                time.sleep(2)  # Check every 2 seconds

        except KeyboardInterrupt:
            print(f"\n\n{'='*70}")
            print("  SYSTEM SHUTDOWN")
            print(f"  Total alerts: {self.alert.alerts_sent}")
            print("="*70 + "\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Default to monitoring Downloads folder
    downloads_path = os.path.expanduser("~/Downloads")

    # Check if path exists
    if not os.path.exists(downloads_path):
        print(f"Error: {downloads_path} does not exist")
        print("Creating Downloads folder...")
        os.makedirs(downloads_path)

    # Start the system
    system = AgenticSecuritySystem(downloads_path)
    system.run()
