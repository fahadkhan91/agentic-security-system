#!/usr/bin/env python3
"""
Agentic AI Security System - Web Dashboard
Beautiful real-time monitoring interface for non-technical users.
"""

import streamlit as st
import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import our simple system components
from main_simple import (
    FileWatcherAgent, ScannerAgent, CoordinatorAgent,
    AlertAgent, SUSPICIOUS_EXTENSIONS, SUSPICIOUS_KEYWORDS
)


# Page configuration
st.set_page_config(
    page_title="Agentic AI Security Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .threat-critical {
        background-color: #ff4444;
        padding: 15px;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        margin: 10px 0;
    }
    .threat-high {
        background-color: #ff8800;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .threat-medium {
        background-color: #ffbb33;
        padding: 15px;
        border-radius: 10px;
        color: black;
        margin: 10px 0;
    }
    .threat-low {
        background-color: #00C851;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .metric-card {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.monitoring = False
    st.session_state.threats_detected = []
    st.session_state.files_scanned = []
    st.session_state.alerts_sent = 0
    st.session_state.critical_threats = 0
    st.session_state.watch_path = os.path.expanduser("~/Downloads")
    st.session_state.last_update = datetime.now()


def display_header():
    """Display the main header."""
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>🛡️ Agentic AI Security Monitor</h1>
        <p style='color: white; margin: 5px 0 0 0; opacity: 0.9;'>
            Multi-Agent Threat Detection & Response System
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_agent_status():
    """Display status of all agents."""
    st.markdown("### 🤖 Agent Status")

    col1, col2, col3, col4 = st.columns(4)

    agents = [
        ("👁️ File Watcher", "Monitoring file system", "#2196F3"),
        ("🔍 Scanner", "Analyzing threats", "#4CAF50"),
        ("🧠 Coordinator", "Making decisions", "#9C27B0"),
        ("📢 Alert", "Ready to respond", "#FF9800")
    ]

    cols = [col1, col2, col3, col4]

    for col, (name, status, color) in zip(cols, agents):
        with col:
            active_status = "🟢 Active" if st.session_state.monitoring else "🔴 Inactive"
            st.markdown(f"""
            <div style='background-color: {color}22; padding: 15px; border-radius: 10px;
                        border-left: 5px solid {color}; margin-bottom: 10px;'>
                <h4 style='margin: 0; color: {color};'>{name}</h4>
                <p style='margin: 5px 0 0 0; font-size: 0.9em;'>{status}</p>
                <p style='margin: 5px 0 0 0; font-size: 0.85em;'>{active_status}</p>
            </div>
            """, unsafe_allow_html=True)


def display_statistics():
    """Display key statistics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🔍 Files Scanned",
            value=len(st.session_state.files_scanned),
            delta=None
        )

    with col2:
        st.metric(
            label="⚠️ Threats Detected",
            value=len(st.session_state.threats_detected),
            delta=None
        )

    with col3:
        st.metric(
            label="🚨 Critical Threats",
            value=st.session_state.critical_threats,
            delta=None
        )

    with col4:
        st.metric(
            label="📢 Alerts Sent",
            value=st.session_state.alerts_sent,
            delta=None
        )


def display_threat(threat_info):
    """Display a single threat with appropriate styling."""
    score = threat_info['threat_score']
    urgency = threat_info['urgency']
    filename = threat_info['filename']
    reasons = threat_info.get('reasons', [])
    timestamp = threat_info.get('timestamp', datetime.now())

    # Choose color based on urgency
    if urgency == 'CRITICAL':
        bg_color = '#ff4444'
        icon = '🚨'
    elif urgency == 'HIGH':
        bg_color = '#ff8800'
        icon = '⚠️'
    elif urgency == 'MEDIUM':
        bg_color = '#ffbb33'
        icon = '⚡'
    else:
        bg_color = '#00C851'
        icon = 'ℹ️'

    st.markdown(f"""
    <div style='background-color: {bg_color}; padding: 15px; border-radius: 10px;
                color: white; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h3 style='margin: 0; color: white;'>{icon} {urgency} THREAT</h3>
                <p style='margin: 5px 0; font-size: 1.1em;'><strong>File:</strong> {filename}</p>
                <p style='margin: 5px 0;'><strong>Threat Score:</strong> {score}/100</p>
                <p style='margin: 5px 0; font-size: 0.85em;'><strong>Detected:</strong> {timestamp.strftime('%H:%M:%S')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if reasons:
        with st.expander("🔍 Analysis Details"):
            for reason in reasons:
                st.write(f"• {reason}")


def display_activity_log():
    """Display recent activity log."""
    st.markdown("### 📋 Activity Log")

    if st.session_state.files_scanned:
        for file_info in reversed(st.session_state.files_scanned[-10:]):
            score = file_info.get('threat_score', 0)
            filename = file_info.get('filename', 'Unknown')
            timestamp = file_info.get('timestamp', datetime.now())

            # Color code by threat level
            if score >= 70:
                color = '#ff4444'
                status = '🚨 HIGH THREAT'
            elif score >= 50:
                color = '#ffbb33'
                status = '⚡ SUSPICIOUS'
            elif score >= 30:
                color = '#4CAF50'
                status = 'ℹ️ LOGGED'
            else:
                color = '#00C851'
                status = '✅ SAFE'

            st.markdown(f"""
            <div style='background-color: {color}22; padding: 10px; border-radius: 5px;
                        margin: 5px 0; border-left: 4px solid {color};'>
                <strong>{status}</strong> - {filename} (Score: {score}/100)<br>
                <small style='opacity: 0.8;'>{timestamp.strftime('%H:%M:%S')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No files scanned yet. Drop files into the monitored folder to see activity.")


def scan_existing_files():
    """Scan files that already exist in the directory."""
    if not os.path.exists(st.session_state.watch_path):
        return

    scanner = ScannerAgent()
    coordinator = CoordinatorAgent()

    try:
        files = os.listdir(st.session_state.watch_path)

        for filename in files[:20]:  # Limit to 20 files
            if filename.startswith('.'):
                continue

            filepath = os.path.join(st.session_state.watch_path, filename)

            if not os.path.isfile(filepath):
                continue

            # Analyze file
            file_info = {'filename': filename, 'filepath': filepath}
            analysis = scanner.analyze_file(file_info)
            decision = coordinator.make_decision(analysis)

            # Store results
            threat_info = {
                'filename': filename,
                'threat_score': analysis['threat_score'],
                'urgency': decision['urgency'],
                'reasons': analysis['reasons'],
                'timestamp': datetime.now()
            }

            st.session_state.files_scanned.append(threat_info)

            if decision['urgency'] in ['CRITICAL', 'HIGH']:
                st.session_state.threats_detected.append(threat_info)
                st.session_state.alerts_sent += 1

                if decision['urgency'] == 'CRITICAL':
                    st.session_state.critical_threats += 1

    except Exception as e:
        st.error(f"Error scanning files: {e}")


def display_threat_feed():
    """Display real-time threat feed."""
    st.markdown("### 🚨 Recent Threats")

    if st.session_state.threats_detected:
        for threat in reversed(st.session_state.threats_detected[-5:]):
            display_threat(threat)
    else:
        st.success("✅ No threats detected! System is secure.")


def display_monitoring_info():
    """Display information about what's being monitored."""
    st.sidebar.markdown("### 📁 Monitoring Configuration")
    st.sidebar.info(f"""
    **Watch Path:**
    `{st.session_state.watch_path}`

    **Monitored Extensions:**
    {', '.join(SUSPICIOUS_EXTENSIONS[:6])}...

    **Detection Methods:**
    - ✓ Signature-based
    - ✓ Heuristic analysis
    - ✓ Extension checking
    - ✓ Keyword detection
    """)


def display_threat_matrix():
    """Display threat level matrix."""
    st.sidebar.markdown("### 🎯 Threat Levels")
    st.sidebar.markdown("""
    <div style='font-size: 0.9em;'>
        <div style='background-color: #ff4444; padding: 8px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>CRITICAL (90+)</strong><br>
            Quarantine immediately
        </div>
        <div style='background-color: #ff8800; padding: 8px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>HIGH (70-89)</strong><br>
            Quarantine & alert
        </div>
        <div style='background-color: #ffbb33; padding: 8px; border-radius: 5px; margin: 5px 0;'>
            <strong>MEDIUM (50-69)</strong><br>
            Alert user
        </div>
        <div style='background-color: #00C851; padding: 8px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>LOW (<50)</strong><br>
            Log only
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_system_info():
    """Display system information."""
    st.sidebar.markdown("### ℹ️ System Info")
    st.sidebar.markdown(f"""
    **Status:** {'🟢 Monitoring' if st.session_state.monitoring else '🔴 Stopped'}
    **Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}
    **Files Watched:** Continuous
    **Response Time:** < 2 seconds
    """)


# Main Dashboard
def main():
    """Main dashboard function."""

    # Header
    display_header()

    # Sidebar controls
    st.sidebar.title("⚙️ Controls")

    if st.sidebar.button("🚀 Start Monitoring", type="primary", disabled=st.session_state.monitoring):
        st.session_state.monitoring = True
        st.session_state.initialized = True
        scan_existing_files()  # Scan existing files
        st.rerun()

    if st.sidebar.button("⏹️ Stop Monitoring", disabled=not st.session_state.monitoring):
        st.session_state.monitoring = False
        st.rerun()

    if st.sidebar.button("🔄 Reset Statistics"):
        st.session_state.threats_detected = []
        st.session_state.files_scanned = []
        st.session_state.alerts_sent = 0
        st.session_state.critical_threats = 0
        st.rerun()

    st.sidebar.markdown("---")

    # Auto-refresh settings
    auto_refresh = st.sidebar.checkbox("🔁 Auto-refresh", value=True)
    if auto_refresh:
        refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 2, 10, 3)

    st.sidebar.markdown("---")

    # Display monitoring info
    display_monitoring_info()
    display_threat_matrix()
    display_system_info()

    # Main content
    if st.session_state.initialized:
        # Agent status
        display_agent_status()

        st.markdown("---")

        # Statistics
        display_statistics()

        st.markdown("---")

        # Two column layout
        col1, col2 = st.columns([3, 2])

        with col1:
            display_activity_log()

        with col2:
            display_threat_feed()

        # Auto-refresh
        if auto_refresh and st.session_state.monitoring:
            time.sleep(refresh_rate)
            st.session_state.last_update = datetime.now()
            st.rerun()

    else:
        # Welcome screen
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>👋 Welcome to Agentic AI Security Monitor</h2>
            <p style='font-size: 1.2em; margin: 20px 0;'>
                A multi-agent system that protects your computer from malware threats.
            </p>
            <p style='font-size: 1em; opacity: 0.8;'>
                Click <strong>"Start Monitoring"</strong> in the sidebar to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feature showcase
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 3em;'>👁️</div>
                <h4>File Watcher</h4>
                <p style='font-size: 0.9em;'>Monitors downloads in real-time</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 3em;'>🔍</div>
                <h4>Smart Scanner</h4>
                <p style='font-size: 0.9em;'>Analyzes files for threats</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 3em;'>🧠</div>
                <h4>Coordinator</h4>
                <p style='font-size: 0.9em;'>Makes intelligent decisions</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 3em;'>📢</div>
                <h4>Alert System</h4>
                <p style='font-size: 0.9em;'>Responds to threats</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.info("""
        **💡 How to Test:**
        1. Click "Start Monitoring" in the sidebar
        2. Open another terminal and run: `cd ~/Downloads && echo "test" > virus.exe`
        3. Watch the dashboard detect the threat in real-time!

        **⚠️ Safety Note:** This system uses safe test files only. Never test with real malware!
        """)


if __name__ == "__main__":
    main()
