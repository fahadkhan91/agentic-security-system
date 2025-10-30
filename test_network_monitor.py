#!/usr/bin/env python3
"""
Test Network Monitor Agent
Tests connection monitoring and threat feed integration.
"""

import yaml
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.network_monitor_agent import NetworkMonitorAgent


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    if not os.path.exists(config_path):
        print("❌ Error: config.yaml not found")
        print("   Copy config.yaml.example to config.yaml and configure network monitoring")
        return None

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('network_monitoring', {})
    except Exception as e:
        print(f"❌ Error loading config.yaml: {e}")
        return None


def print_header():
    """Print test header"""
    print("\n" + "=" * 70)
    print("  NETWORK MONITOR TEST")
    print("  Agentic AI Security System")
    print("=" * 70)


def test_feed_loading(agent):
    """Test loading threat feed from SRX server"""
    print("\n📡 Testing SRX Threat Feed...")
    print("-" * 70)

    print(f"Feed URL: {agent.local_feed_url}")

    # Load feed
    ips = agent.load_local_feed()

    if ips:
        print(f"✅ Successfully loaded {len(ips)} IPs from SRX server")
        print(f"\nSample IPs (first 10):")
        for i, ip in enumerate(list(ips)[:10], 1):
            print(f"  {i}. {ip}")

        if len(ips) > 10:
            print(f"  ... and {len(ips) - 10} more")

        return True
    else:
        print("❌ Failed to load threat feed")
        print("\nPossible reasons:")
        print("  • SRX server is not running")
        print("  • URL is incorrect")
        print("  • Network connectivity issues")
        print(f"\nTry: curl {agent.local_feed_url}")
        return False


def test_connection_monitoring(agent):
    """Test active connection monitoring"""
    print("\n🔍 Testing Connection Monitoring...")
    print("-" * 70)

    print("Scanning active connections...")

    # Run one scan cycle
    agent.monitor_connections()

    # Get statistics
    stats = agent.get_statistics()

    print(f"\n📊 Statistics:")
    print(f"  Total connections checked: {stats['total_connections']}")
    print(f"  Unique IPs seen: {stats['unique_ips_seen']}")
    print(f"  Blacklisted IPs: {stats['blacklist_size']}")
    print(f"  Malicious connections: {stats['blocked_connections']}")

    # Show recent threats
    threats = agent.get_recent_threats()
    if threats:
        print(f"\n🚨 Malicious Connections Detected:")
        for threat in threats:
            print(f"\n  ⚠️  Alert:")
            print(f"    IP: {threat['ip']}:{threat['port']}")
            print(f"    Process: {threat['process_name']} (PID: {threat['process_pid']})")
            print(f"    Time: {threat['timestamp'].strftime('%H:%M:%S')}")
            print(f"    Score: {threat['threat_score']}/100")
    else:
        print("\n✅ No malicious connections detected")

    return True


def test_ip_check(agent):
    """Test IP reputation checking"""
    print("\n🔎 Testing IP Reputation Check...")
    print("-" * 70)

    # Test IPs
    test_ips = [
        ("8.8.8.8", "Google DNS (should be clean)"),
        ("127.0.0.1", "Localhost (should be ignored)"),
    ]

    # Add one IP from blacklist if available
    if agent.ip_blacklist:
        test_ip = list(agent.ip_blacklist)[0]
        test_ips.append((test_ip, "From blacklist (should be malicious)"))

    for ip, description in test_ips:
        print(f"\nChecking: {ip} - {description}")
        result = agent.check_ip_reputation(ip)

        if result['malicious']:
            print(f"  🚨 MALICIOUS")
            print(f"  Source: {result['source']}")
            print(f"  Confidence: {result['confidence']}%")
        else:
            print(f"  ✅ Clean")


def print_summary(agent):
    """Print summary and instructions"""
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)

    stats = agent.get_statistics()

    print(f"\n📊 Network Monitor Status:")
    print(f"  Enabled: {'✅ Yes' if agent.enabled else '❌ No'}")
    print(f"  Threat Feed: {agent.local_feed_url}")
    print(f"  Blacklist Size: {stats['blacklist_size']} IPs")
    print(f"  Scan Interval: {agent.scan_interval} seconds")

    if stats['last_feed_update']:
        print(f"  Last Update: {stats['last_feed_update']}")

    print(f"\n💡 Integration Status:")

    if stats['blacklist_size'] > 0:
        print(f"  ✅ SRX threat feed: Connected ({stats['blacklist_size']} IPs loaded)")
    else:
        print(f"  ⚠️  SRX threat feed: Not loaded")
        print(f"     Check: curl {agent.local_feed_url}")

    print(f"\n📝 To enable in dashboard:")
    print(f"  1. Edit config.yaml")
    print(f"  2. Set network_monitoring.enabled: true")
    print(f"  3. Restart dashboard: python3 -m streamlit run dashboard.py")

    print(f"\n🔗 Your SRX feed URL:")
    print(f"  {agent.local_feed_url}")

    print("\n" + "=" * 70)


def main():
    """Main test function"""
    print_header()

    # Load configuration
    print("\n🔧 Loading configuration...")
    config = load_config()

    if not config:
        print("\n❌ Cannot proceed without config.yaml")
        print("\n📖 Setup instructions:")
        print("   1. Copy config.yaml.example to config.yaml")
        print("   2. Edit network_monitoring section")
        print("   3. Set your SRX feed URL (default: http://localhost/srx/custom-feed.txt)")
        return

    # Create network monitor agent
    print("✅ Config loaded")

    # Override enabled flag for testing
    config['enabled'] = True

    print(f"\n🚀 Initializing Network Monitor Agent...")
    agent = NetworkMonitorAgent(config)

    print(f"✅ Agent initialized")

    # Test 1: Load threat feed
    feed_ok = test_feed_loading(agent)

    # Test 2: Monitor connections
    if feed_ok:
        test_connection_monitoring(agent)

        # Test 3: IP reputation check
        test_ip_check(agent)

    # Print summary
    print_summary(agent)

    # Show logs
    print(f"\n📝 Recent Activity Logs:")
    for log in agent.get_recent_logs(10):
        timestamp = log['timestamp'].strftime('%H:%M:%S')
        print(f"  [{timestamp}] {log['action']}: {log['details']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
