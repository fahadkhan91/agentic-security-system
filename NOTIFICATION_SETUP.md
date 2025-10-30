# Notification Setup Guide

## 🚀 Three Ways to Get Alerts!

Your security system can now send alerts via:
1. 📧 **Email** - Gmail notifications
2. 📱 **WhatsApp** - Instant messages (FREE!)
3. 🖥️ **Desktop** - Pop-up notifications

---

## Quick Start (5 Minutes)

### Option 1: WhatsApp Only (EASIEST - FREE!)

This is the **recommended option** for hackathons - it's free, fast, and impressive!

**Step 1: Get CallMeBot API Key** (2 minutes)

1. On your phone, add this number to contacts: **+34 644 32 88 08**
   - Save it as "CallMeBot"

2. Open WhatsApp and send this exact message to CallMeBot:
   ```
   I allow callmebot to send me messages
   ```

3. You'll instantly receive your API key. It looks like: `123456`

**Step 2: Configure System** (1 minute)

Edit `config.yaml`:

```yaml
whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"  # Your phone with country code
    apikey: "123456"  # API key from CallMeBot
```

**Step 3: Test It!** (30 seconds)

```bash
python3 test_notifications.py
```

You should receive a WhatsApp message immediately! 🎉

---

## Option 2: Email Alerts (FREE - Requires Gmail)

### Gmail Setup (5 minutes)

**Step 1: Enable 2-Step Verification**

1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the steps to enable it

**Step 2: Generate App Password**

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Enter "Security System"
4. Click "Generate"
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

**Step 3: Configure System**

Edit `config.yaml`:

```yaml
email:
  enabled: true
  from: "your.email@gmail.com"  # Your Gmail
  to: "your.email@gmail.com"  # Where to send (can be same)
  password: "abcd efgh ijkl mnop"  # App password (NOT your Gmail password!)
```

**Step 4: Test It!**

```bash
python3 test_notifications.py
```

Check your email inbox! 📧

---

## Option 3: All Three! (Ultimate Demo)

Configure both WhatsApp AND Email:

```yaml
email:
  enabled: true
  from: "your.email@gmail.com"
  to: "your.email@gmail.com"
  password: "your-app-password"

whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"
    apikey: "123456"

desktop:
  enabled: true
```

Now you'll get alerts on:
- ✅ WhatsApp (instant!)
- ✅ Email (detailed)
- ✅ Desktop (visual)

**This is VERY impressive for hackathons!**

---

## Installation

### Required for Email:
```bash
# Already included in Python, no installation needed!
```

### Required for WhatsApp:
```bash
pip install requests
```

### Required for Desktop Notifications:
```bash
pip install plyer
```

### Install Everything:
```bash
pip install -r requirements.txt
```

Update `requirements.txt`:
```
watchdog==3.0.0
plyer==2.1.0
requests==2.31.0
streamlit==1.31.0
pyyaml==6.0.1
```

---

## Testing Your Setup

### Test Script

Create `test_notifications.py`:

```python
#!/usr/bin/env python3
"""Test notification system"""

import yaml
import sys
sys.path.insert(0, '.')

from agents.notification_agent import NotificationAgent
from datetime import datetime

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Merge all notification configs
notification_config = {
    **config.get('email', {}),
    **config.get('whatsapp', {}).get('callmebot', {}),
    **config.get('desktop', {}),
    'whatsapp_enabled': config.get('whatsapp', {}).get('enabled', False),
    'whatsapp_method': config.get('whatsapp', {}).get('method', 'callmebot'),
    'email_enabled': config.get('email', {}).get('enabled', False),
    'desktop_enabled': config.get('desktop', {}).get('enabled', True)
}

# Create agent
agent = NotificationAgent(notification_config)

print("=" * 70)
print("  NOTIFICATION SYSTEM TEST")
print("=" * 70)
print("\nConfiguration:")
print(f"  Email: {'✓ Enabled' if agent.email_enabled else '✗ Disabled'}")
print(f"  WhatsApp: {'✓ Enabled' if agent.whatsapp_enabled else '✗ Disabled'}")
print(f"  Desktop: {'✓ Enabled' if agent.desktop_enabled else '✗ Disabled'}")
print("\nSending test notifications...\n")

# Send test alert
test_threat = {
    'urgency': 'HIGH',
    'filename': 'test_virus.exe',
    'threat_score': 85,
    'reasons': [
        'This is a TEST notification',
        'High-risk extension: .exe (+40)',
        'Suspicious keyword: virus (+30)',
        'Small file size (+15)'
    ],
    'timestamp': datetime.now()
}

results = agent.send_threat_alert(test_threat)

print("\nResults:")
print(f"  Email: {'✓ Sent' if results.get('email') else '✗ Failed'}")
print(f"  WhatsApp: {'✓ Sent' if results.get('whatsapp') else '✗ Failed'}")
print(f"  Desktop: {'✓ Sent' if results.get('desktop') else '✗ Failed'}")
print("\n" + "=" * 70)

if results.get('whatsapp'):
    print("\n🎉 Check your WhatsApp for the test message!")
if results.get('email'):
    print("📧 Check your email inbox!")
if results.get('desktop'):
    print("🖥️ Check for desktop notification!")
```

**Run it**:
```bash
python3 test_notifications.py
```

---

## Troubleshooting

### WhatsApp Not Working

**Problem**: "Missing CallMeBot configuration"
**Fix**: Make sure you have both phone number AND API key in config.yaml

**Problem**: No message received
**Fix**:
1. Check phone number has country code (e.g., +92 for Pakistan)
2. Remove spaces from phone number
3. Wait 30 seconds (sometimes delayed)
4. Check you sent the activation message to CallMeBot

**Problem**: "requests module not found"
**Fix**: `pip install requests`

### Email Not Working

**Problem**: "Authentication failed"
**Fix**:
1. Use App Password, NOT your Gmail password
2. Make sure 2-Step Verification is enabled
3. Generate a new App Password

**Problem**: "SMTP connection failed"
**Fix**: Check your internet connection

### Desktop Notification Not Working

**Problem**: No pop-up appears
**Fix**:
1. Install plyer: `pip install plyer`
2. Check system notification settings
3. On Linux, may need: `sudo apt-get install python3-notify2`

---

## Demo Strategy

### For Hackathon Presentations

**Opening Line**:
"When the system detects a threat, it doesn't just log it - it immediately alerts you via WhatsApp, email, and desktop notification."

**Live Demo**:
1. Start the system
2. Create `virus.exe`
3. Show detection on screen
4. **Pull out your phone**
5. Show WhatsApp message in real-time!
6. "See? I got the alert on my phone instantly!"

**Why This is Impressive**:
- Real-world practical
- Multi-channel communication
- Instant notification
- Shows complete system
- Very professional

---

## Security Notes

### Protecting Your Credentials

**Never commit config.yaml with real passwords!**

Create `.gitignore`:
```
config.yaml
*.pyc
__pycache__/
.env
```

**For demos**, use a demo email account:
- Create throwaway Gmail just for demos
- Don't use your personal email/phone

**App Passwords are safer**:
- Not your real Gmail password
- Can be revoked anytime
- Specific to this app only

---

## Configuration Examples

### Minimal Setup (WhatsApp Only)

```yaml
email:
  enabled: false

whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"
    apikey: "123456"

desktop:
  enabled: true
```

### Full Setup (Everything)

```yaml
email:
  enabled: true
  from: "demo@gmail.com"
  to: "demo@gmail.com"
  password: "abcd efgh ijkl mnop"
  smtp_server: "smtp.gmail.com"
  smtp_port: 587

whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"
    apikey: "123456"

desktop:
  enabled: true

monitoring:
  watch_folders:
    - "~/Downloads"
  notification_threshold: 50
```

### Demo-Safe Setup

```yaml
# For public demos - doesn't expose real credentials
email:
  enabled: false  # Disable to avoid showing password

whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"
    apikey: "123456"

desktop:
  enabled: true
```

---

## Advanced: Twilio WhatsApp (Optional)

Only use if you already have Twilio account.

### Setup:
1. Create account at https://www.twilio.com/
2. Get Account SID and Auth Token
3. Set up WhatsApp Sandbox or get approved number

### Config:
```yaml
whatsapp:
  enabled: true
  method: "twilio"
  twilio:
    account_sid: "ACxxxxxxxxxxxx"
    auth_token: "your_auth_token"
    from: "+14155238886"  # Twilio sandbox number
    to: "+923001234567"  # Your number
```

**Note**: CallMeBot is recommended - it's free and works great!

---

## What the Notifications Look Like

### WhatsApp Message:
```
🚨 SECURITY ALERT 🚨

Threat Level: HIGH
File: virus.exe
Threat Score: 85/100
Detected: 2025-01-29 14:23:45

Analysis:
• High-risk extension: .exe (+40)
• Suspicious keyword: virus (+30)
• Small file size (+15)

Action: File has been flagged for quarantine.

---
Agentic AI Security System
Multi-Agent Threat Detection
```

### Email:
- **Subject**: 🚨 HIGH THREAT DETECTED: virus.exe
- **Body**: Same as WhatsApp message above
- **From**: Your configured email
- **To**: Your configured recipient

### Desktop:
- **Title**: ⚠️ HIGH THREAT DETECTED: virus.exe
- **Message**: File virus.exe detected with threat score 85/100...
- **Duration**: 10 seconds
- **Style**: System notification popup

---

## Why This Makes Your Project Better

### Before:
- System detects threats
- Shows in terminal/dashboard
- ✅ Good

### After (With Notifications):
- System detects threats
- Shows in terminal/dashboard
- **Sends WhatsApp message**
- **Sends email alert**
- **Shows desktop popup**
- ✅✅✅ **AMAZING!**

### For Judges:
"This isn't just a monitoring tool - it's a complete alert system. When a threat is detected, I'm notified immediately on my phone via WhatsApp, I get an email with full details, and there's a desktop notification. This makes it practical for real-world use."

---

## Quick Reference

### Just Want WhatsApp? (Fastest)
1. Message CallMeBot: +34 644 32 88 08
2. Send: "I allow callmebot to send me messages"
3. Get API key
4. Edit config.yaml
5. `python3 test_notifications.py`
6. Done! ✅

### Just Want Email?
1. Enable Gmail 2-Step
2. Generate App Password
3. Edit config.yaml
4. `python3 test_notifications.py`
5. Done! ✅

### Want Both?
1. Do both above
2. Set both to `enabled: true`
3. `python3 test_notifications.py`
4. Done! ✅✅

---

## Next Steps

1. **Choose your method** (WhatsApp recommended!)
2. **Follow setup steps** (5 minutes)
3. **Test it** (`python3 test_notifications.py`)
4. **Integrate with dashboard** (already done!)
5. **Practice demo** (show phone notification live!)

Your security system is now **production-ready** with multi-channel alerting! 🎉

---

## Support

Having trouble? Check:
1. Config.yaml syntax (proper spacing matters in YAML)
2. Phone number includes country code (+92...)
3. API key is correct (no spaces)
4. Internet connection working
5. pip packages installed

Still stuck? The test script will show detailed error messages!
