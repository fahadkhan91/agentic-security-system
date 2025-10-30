#!/usr/bin/env python3
"""
Quick WhatsApp Test - No Input Required
Sends test WhatsApp notification immediately
"""

import yaml
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.notification_agent import NotificationAgent

print("=" * 70)
print("  WHATSAPP TEST - SENDING NOW!")
print("=" * 70)

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create notification config
notification_config = {
    'whatsapp_enabled': config.get('whatsapp', {}).get('enabled', False),
    'whatsapp_method': config.get('whatsapp', {}).get('method', 'callmebot'),
    'callmebot_phone': config.get('whatsapp', {}).get('callmebot', {}).get('phone', ''),
    'callmebot_apikey': config.get('whatsapp', {}).get('callmebot', {}).get('apikey', ''),
    'desktop_enabled': True,
    'email_enabled': False
}

print(f"\n📱 WhatsApp Configuration:")
print(f"   Enabled: {notification_config['whatsapp_enabled']}")
print(f"   Phone: {notification_config['callmebot_phone']}")
print(f"   API Key: {'*' * len(notification_config['callmebot_apikey'])} (configured)")

# Create agent
agent = NotificationAgent(notification_config)

# Create test threat
test_threat = {
    'urgency': 'HIGH',
    'filename': 'test_virus.exe',
    'threat_score': 85,
    'reasons': [
        '⚠️ This is a TEST notification from your Security System',
        'Testing WhatsApp integration',
        'If you receive this, WhatsApp is working perfectly!'
    ],
    'timestamp': datetime.now()
}

print("\n🚀 Sending WhatsApp test message...")
print("-" * 70)

# Send alert
results = agent.send_threat_alert(test_threat)

print("\n📊 Result:")
print("-" * 70)

if results.get('whatsapp'):
    print(f"✅ SUCCESS! WhatsApp message sent to {notification_config['callmebot_phone']}")
    print(f"\n📱 CHECK YOUR PHONE NOW!")
    print(f"   Open WhatsApp and look for a message from CallMeBot")
    print(f"   It should contain the security alert details")
else:
    print(f"❌ FAILED to send WhatsApp message")
    print(f"\nPossible issues:")
    print(f"   • Check phone number: {notification_config['callmebot_phone']}")
    print(f"   • Check API key is correct")
    print(f"   • Make sure you sent activation message to CallMeBot")
    print(f"   • Wait 30 seconds and check phone again")

if results.get('desktop'):
    print(f"\n🖥️ Desktop notification also sent!")

print("\n" + "=" * 70)

# Show logs
print("\n📝 Detailed logs:")
for log in agent.get_recent_logs(5):
    print(f"   [{log['timestamp'].strftime('%H:%M:%S')}] {log['action']}: {log['details']}")

print("\n" + "=" * 70)
