#!/usr/bin/env python3
"""
Test Notification System
Sends test alerts via Email, WhatsApp, and Desktop
"""

import yaml
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.notification_agent import NotificationAgent


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    if not os.path.exists(config_path):
        print(f"❌ Error: config.yaml not found at {config_path}")
        print("\nPlease create config.yaml with your notification settings.")
        print("See NOTIFICATION_SETUP.md for instructions.")
        return None

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ Error loading config.yaml: {e}")
        return None


def create_notification_config(config):
    """Create notification agent configuration from config file"""
    notification_config = {}

    # Email settings
    email_config = config.get('email', {})
    notification_config['email_enabled'] = email_config.get('enabled', False)
    notification_config['email_from'] = email_config.get('from', '')
    notification_config['email_to'] = email_config.get('to', '')
    notification_config['email_password'] = email_config.get('password', '')
    notification_config['smtp_server'] = email_config.get('smtp_server', 'smtp.gmail.com')
    notification_config['smtp_port'] = email_config.get('smtp_port', 587)

    # WhatsApp settings
    whatsapp_config = config.get('whatsapp', {})
    notification_config['whatsapp_enabled'] = whatsapp_config.get('enabled', False)
    notification_config['whatsapp_method'] = whatsapp_config.get('method', 'callmebot')

    # CallMeBot
    callmebot_config = whatsapp_config.get('callmebot', {})
    notification_config['callmebot_phone'] = callmebot_config.get('phone', '')
    notification_config['callmebot_apikey'] = callmebot_config.get('apikey', '')

    # Twilio
    twilio_config = whatsapp_config.get('twilio', {})
    notification_config['twilio_account_sid'] = twilio_config.get('account_sid', '')
    notification_config['twilio_auth_token'] = twilio_config.get('auth_token', '')
    notification_config['twilio_from'] = twilio_config.get('from', '')
    notification_config['twilio_to'] = twilio_config.get('to', '')

    # Desktop settings
    desktop_config = config.get('desktop', {})
    notification_config['desktop_enabled'] = desktop_config.get('enabled', True)

    return notification_config


def print_header():
    """Print test header"""
    print("\n" + "=" * 70)
    print("  NOTIFICATION SYSTEM TEST")
    print("  Agentic AI Security System")
    print("=" * 70)


def print_configuration(agent):
    """Print current configuration"""
    print("\n📋 Configuration Status:")
    print("-" * 70)

    # Email
    print(f"\n📧 Email Notifications:")
    if agent.email_enabled:
        print(f"   Status: ✓ ENABLED")
        print(f"   From: {agent.email_from}")
        print(f"   To: {agent.email_to}")
        print(f"   Server: {agent.smtp_server}:{agent.smtp_port}")
        if agent.email_password:
            print(f"   Password: {'*' * len(agent.email_password)} (configured)")
        else:
            print(f"   Password: ❌ NOT SET")
    else:
        print(f"   Status: ✗ DISABLED")
        print(f"   (Set email.enabled: true in config.yaml)")

    # WhatsApp
    print(f"\n📱 WhatsApp Notifications:")
    if agent.whatsapp_enabled:
        print(f"   Status: ✓ ENABLED")
        print(f"   Method: {agent.whatsapp_method}")
        if agent.whatsapp_method == 'callmebot':
            print(f"   Phone: {agent.callmebot_phone}")
            if agent.callmebot_apikey:
                print(f"   API Key: {'*' * len(agent.callmebot_apikey)} (configured)")
            else:
                print(f"   API Key: ❌ NOT SET")
        elif agent.whatsapp_method == 'twilio':
            print(f"   From: {agent.twilio_from}")
            print(f"   To: {agent.twilio_to}")
            if agent.twilio_account_sid:
                print(f"   Account SID: {agent.twilio_account_sid[:8]}... (configured)")
            else:
                print(f"   Account SID: ❌ NOT SET")
    else:
        print(f"   Status: ✗ DISABLED")
        print(f"   (Set whatsapp.enabled: true in config.yaml)")

    # Desktop
    print(f"\n🖥️  Desktop Notifications:")
    if agent.desktop_enabled:
        print(f"   Status: ✓ ENABLED")
        try:
            from plyer import notification
            print(f"   Plyer: ✓ Available")
        except ImportError:
            print(f"   Plyer: ❌ NOT INSTALLED (pip install plyer)")
    else:
        print(f"   Status: ✗ DISABLED")

    print("\n" + "-" * 70)


def send_test_alert(agent):
    """Send test threat alert"""
    print("\n🔔 Sending test notifications...")
    print("-" * 70)

    # Create test threat
    test_threat = {
        'urgency': 'HIGH',
        'filename': 'test_virus.exe',
        'threat_score': 85,
        'reasons': [
            '⚠️  This is a TEST notification from your security system',
            'High-risk extension: .exe (+40)',
            'Suspicious keyword: virus (+30)',
            'Small file size (+15)'
        ],
        'timestamp': datetime.now()
    }

    # Send alerts
    results = agent.send_threat_alert(test_threat)

    # Print results
    print("\n📊 Results:")
    print("-" * 70)

    channels_sent = 0

    if agent.email_enabled:
        if results.get('email'):
            print(f"   📧 Email: ✓ SENT to {agent.email_to}")
            channels_sent += 1
        else:
            print(f"   📧 Email: ✗ FAILED (check configuration and logs)")

    if agent.whatsapp_enabled:
        if results.get('whatsapp'):
            phone = agent.callmebot_phone if agent.whatsapp_method == 'callmebot' else agent.twilio_to
            print(f"   📱 WhatsApp: ✓ SENT to {phone}")
            channels_sent += 1
        else:
            print(f"   📱 WhatsApp: ✗ FAILED (check configuration and logs)")

    if agent.desktop_enabled:
        if results.get('desktop'):
            print(f"   🖥️  Desktop: ✓ SENT")
            channels_sent += 1
        else:
            print(f"   🖥️  Desktop: ✗ FAILED (check if plyer is installed)")

    print("-" * 70)

    return channels_sent


def print_instructions(agent, channels_sent):
    """Print next steps based on results"""
    print(f"\n✅ Successfully sent {channels_sent} notification(s)!\n")

    if channels_sent > 0:
        print("👀 Check for notifications:")

        if agent.email_enabled:
            print(f"   📧 Check email inbox: {agent.email_to}")

        if agent.whatsapp_enabled:
            phone = agent.callmebot_phone if agent.whatsapp_method == 'callmebot' else agent.twilio_to
            print(f"   📱 Check WhatsApp on: {phone}")

        if agent.desktop_enabled:
            print(f"   🖥️  Check for desktop popup notification")

    else:
        print("ℹ️  No notifications were sent.")
        print("\nPossible reasons:")
        print("   • No notification methods are enabled in config.yaml")
        print("   • Missing credentials (email password, WhatsApp API key)")
        print("   • Configuration errors\n")
        print("📖 See NOTIFICATION_SETUP.md for setup instructions")

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
        print("   2. Edit config.yaml with your settings")
        print("   3. See NOTIFICATION_SETUP.md for detailed instructions")
        return

    # Create notification agent
    notification_config = create_notification_config(config)
    agent = NotificationAgent(notification_config)

    # Print configuration
    print_configuration(agent)

    # Check if anything is enabled
    if not any([agent.email_enabled, agent.whatsapp_enabled, agent.desktop_enabled]):
        print("\n⚠️  WARNING: All notification methods are disabled!")
        print("   Enable at least one method in config.yaml")
        print("   Example: Set 'enabled: true' under email or whatsapp")
        return

    # Ask for confirmation
    print("\n❓ Ready to send test notifications?")
    response = input("   Press Enter to continue, or Ctrl+C to cancel: ")

    # Send test alert
    channels_sent = send_test_alert(agent)

    # Print instructions
    print_instructions(agent, channels_sent)

    # Show logs if failures
    if channels_sent == 0 or (agent.email_enabled and not agent.notifications_sent['email']):
        print("\n📝 Recent logs:")
        for log in agent.get_recent_logs(5):
            print(f"   [{log['timestamp'].strftime('%H:%M:%S')}] {log['action']}: {log['details']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
