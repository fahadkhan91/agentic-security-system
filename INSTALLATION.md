# Installation Guide

> Complete setup instructions for running the Agentic AI Security Monitoring System on your machine

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
4. [Configuration Setup](#configuration-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Updating the Application](#updating-the-application)

---

## 📌 System Requirements

### Operating System
- ✅ **Linux** (Ubuntu 20.04+, Debian, Fedora, etc.)
- ✅ **macOS** (10.15+)
- ✅ **Windows** (10/11 with WSL2 recommended)

### Software Requirements
- **Python**: 3.7 or higher (3.11 recommended)
- **pip**: Python package manager
- **git**: For cloning the repository

### Hardware Requirements
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB free space
- **Internet**: Required for downloading dependencies and sending notifications

---

## 🚀 Quick Start

For experienced users who want to get started quickly:

```bash
# 1. Clone the repository
git clone https://github.com/fahadkhan91/agentic-security-system.git
cd agentic-security-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure notifications
cp config.yaml.example config.yaml
nano config.yaml  # Edit with your credentials

# 4. Run the dashboard
python3 -m streamlit run dashboard.py
```

---

## 📦 Detailed Installation

### Step 1: Install Python

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install python3 python3-pip git -y
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3 git
```

#### Windows
1. Download Python from https://www.python.org/downloads/
2. Run installer and **check "Add Python to PATH"**
3. Install Git from https://git-scm.com/download/win
4. Open Command Prompt or PowerShell

### Step 2: Verify Installation

```bash
# Check Python version (should be 3.7+)
python3 --version

# Check pip
pip3 --version

# Check git
git --version
```

### Step 3: Clone the Repository

```bash
# Choose a directory where you want to install
cd ~  # or cd /path/to/your/projects

# Clone the repository
git clone https://github.com/fahadkhan91/agentic-security-system.git

# Navigate into the directory
cd agentic-security-system

# Verify files
ls -la
```

You should see:
```
├── agents/
├── detection/
├── dashboard.py
├── main_simple.py
├── test_notifications.py
├── config.yaml.example
├── requirements.txt
├── README.md
└── ... (other files)
```

### Step 4: Create Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Your prompt should now show (venv)
```

### Step 5: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

You should see packages like:
- streamlit
- watchdog
- pyyaml
- requests
- plyer

---

## ⚙️ Configuration Setup

### Step 1: Create Your Configuration File

```bash
# Copy the example configuration
cp config.yaml.example config.yaml

# Open for editing
nano config.yaml  # or use your favorite editor: vim, code, gedit, etc.
```

### Step 2: Configure Email Notifications (Optional)

#### Get Gmail App Password:
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (required)
3. Go to https://myaccount.google.com/apppasswords
4. Generate an app password for "Mail"
5. Copy the 16-character password

#### Edit config.yaml:
```yaml
email:
  enabled: true
  from: "your-email@gmail.com"
  to: "recipient@gmail.com"
  password: "your-16-char-app-password"  # NOT your regular password!
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
```

**Important:** Use the App Password, NOT your regular Gmail password!

### Step 3: Configure WhatsApp Notifications (Optional)

#### Option A: CallMeBot (FREE - No Credit Card!)

1. Add **+34 644 32 88 08** to your phone contacts as "CallMeBot"
2. Send this message to CallMeBot on WhatsApp:
   ```
   I allow callmebot to send me messages
   ```
3. You'll receive your API key immediately (it's a number like "123456")
4. Edit config.yaml:

```yaml
whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+1234567890"  # Your phone number with country code
    apikey: "123456"       # The API key you received
```

#### Option B: Twilio (PAID - Requires Account)

Only use if you already have a Twilio account:

```yaml
whatsapp:
  enabled: true
  method: "twilio"
  twilio:
    account_sid: "your_account_sid"
    auth_token: "your_auth_token"
    from: "+1234567890"  # Your Twilio WhatsApp number
    to: "+1234567890"    # Recipient's number
```

### Step 4: Configure Desktop Notifications

Desktop notifications are enabled by default:

```yaml
desktop:
  enabled: true  # Set to false if you don't want desktop popups
```

### Step 5: Save and Test Configuration

```bash
# Save the file (Ctrl+O in nano, :wq in vim)

# Test your notification setup
python3 test_notifications.py
```

If configured correctly, you should receive test notifications!

---

## 🎮 Running the Application

### Option 1: Web Dashboard (Recommended)

The dashboard provides a beautiful web interface:

```bash
# Start the dashboard
python3 -m streamlit run dashboard.py

# Or if using virtual environment:
streamlit run dashboard.py
```

**Access the dashboard:**
- Open browser and go to: http://localhost:8501
- Click **"Start Monitoring"** in the sidebar
- Check **"Enable Notifications"** to receive alerts

**To stop:** Press `Ctrl+C` in the terminal

### Option 2: Command Line Interface

The CLI version shows output in the terminal:

```bash
# Start monitoring
python3 main_simple.py

# By default, monitors ~/Downloads folder
```

**To stop:** Press `Ctrl+C`

### Option 3: Test Mode

Test the system without waiting for real files:

```bash
# Test notifications
python3 test_notifications.py

# Create a test malware file
cd ~/Downloads
echo "test" > virus.exe

# Watch the system detect it!
```

---

## 🧪 Verifying Installation

### Test 1: Basic Functionality

```bash
# Should show no errors
python3 -c "import streamlit; import yaml; import watchdog; print('✅ All imports working')"
```

### Test 2: Configuration Loading

```bash
# Should show your settings
python3 -c "import yaml; c=yaml.safe_load(open('config.yaml')); print('✅ Config loaded'); print(f'Email: {c[\"email\"][\"enabled\"]}'); print(f'WhatsApp: {c[\"whatsapp\"][\"enabled\"]}')"
```

### Test 3: Dashboard Launch

```bash
# Start dashboard (should open browser automatically)
python3 -m streamlit run dashboard.py
```

### Test 4: Threat Detection

```bash
# In another terminal, create test file
cd ~/Downloads
echo "malware test" > dangerous_virus.exe

# Dashboard should detect it within 2-3 seconds
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure you're in the project directory
cd /path/to/agentic-security-system

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# If using virtual environment, make sure it's activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
```

### Issue: "config.yaml not found"

**Solution:**
```bash
# Check if file exists
ls -la config.yaml

# If not, copy from example
cp config.yaml.example config.yaml

# Edit with your credentials
nano config.yaml
```

### Issue: Email notifications not working

**Checklist:**
- ✅ Using Gmail App Password (NOT regular password)
- ✅ 2-Step Verification enabled on Gmail
- ✅ App Password is 16 characters (no spaces)
- ✅ Email and password are in quotes in config.yaml
- ✅ `enabled: true` (not `enabled: false`)

**Test:**
```bash
python3 test_notifications.py
```

### Issue: WhatsApp notifications not working

**For CallMeBot:**
- ✅ Added +34 644 32 88 08 to contacts
- ✅ Sent activation message to CallMeBot
- ✅ Received API key (6-digit number)
- ✅ Phone number includes country code (e.g., +1 for US, +966 for Saudi Arabia)

**Test:**
```bash
python3 test_notifications.py
```

### Issue: Dashboard not detecting files

**Solution:**
```bash
# 1. Check if monitoring is started
# Look for "🟢 Active" status in dashboard

# 2. Check if "Enable Notifications" is checked
# (Required for sending alerts)

# 3. Verify watch path
# Default is ~/Downloads
# Make sure this folder exists

# 4. Check file has suspicious name
# Examples: virus.exe, malware.bat, trojan.scr
```

### Issue: "Permission denied" errors

**Linux/macOS:**
```bash
# Make scripts executable
chmod +x dashboard.py main_simple.py test_notifications.py

# If watching system folders, run with sudo (not recommended)
# Better: use ~/Downloads or ~/Desktop
```

### Issue: Port 8501 already in use

**Solution:**
```bash
# Use a different port
streamlit run dashboard.py --server.port 8502

# Or kill the existing process
pkill -f streamlit
```

### Issue: Desktop notifications not showing

**Linux:**
```bash
# Install notification dependencies
sudo apt install libnotify-bin

# Test desktop notifications
notify-send "Test" "This is a test notification"
```

**macOS:**
```bash
# Make sure Python has notification permissions
# System Preferences → Security & Privacy → Privacy → Notifications
```

**Windows:**
```bash
# Install plyer
pip install plyer

# Make sure notifications are enabled in Windows settings
```

---

## 🔄 Updating the Application

### Pull Latest Changes from GitHub

```bash
# Navigate to project directory
cd /path/to/agentic-security-system

# Pull latest updates
git pull origin main

# Update dependencies (if requirements.txt changed)
pip install -r requirements.txt --upgrade

# Restart the application
```

### Check for Updates

```bash
# Check current version
git log --oneline -1

# See what's new
git log --oneline -5

# View all commits
git log --graph --oneline --all
```

---

## 📂 Project Structure

```
agentic-security-system/
│
├── 📁 agents/                    # Agent modules
│   ├── base_agent.py            # Base agent class
│   ├── file_watcher.py          # File monitoring
│   └── notification_agent.py    # Email/WhatsApp/Desktop alerts
│
├── 📁 detection/                 # Threat detection
│   └── signatures.py            # Malware signatures
│
├── 🌐 dashboard.py              # Web interface (MAIN APP)
├── 🖥️  main_simple.py           # CLI version
├── 🧪 test_notifications.py     # Test your setup
│
├── ⚙️  config.yaml              # Your credentials (create from example)
├── ⚙️  config.yaml.example      # Configuration template
├── 📦 requirements.txt          # Python dependencies
│
└── 📖 Documentation
    ├── README.md                # Main documentation
    ├── INSTALLATION.md          # This file
    ├── NOTIFICATION_SETUP.md    # Detailed notification guide
    └── GITHUB_SETUP.md          # Git repository info
```

---

## 🎯 Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp config.yaml.example config.yaml && nano config.yaml

# Run dashboard
python3 -m streamlit run dashboard.py

# Run CLI version
python3 main_simple.py

# Test notifications
python3 test_notifications.py

# Test with sample malware
cd ~/Downloads && echo "test" > virus.exe

# Update from git
git pull origin main

# Check status
git status
```

---

## 🔒 Security Notes

### What's Stored Where:

| File | Contains | In Git? | Purpose |
|------|----------|---------|---------|
| `config.yaml` | Your credentials | ❌ NO | Your personal config |
| `config.yaml.example` | Template only | ✅ YES | Guide for setup |
| Source code | No secrets | ✅ YES | Application logic |

### Best Practices:

1. **Never commit config.yaml** to git (it's in .gitignore)
2. **Use App Passwords** for Gmail (not your regular password)
3. **Keep credentials private** - don't share your config.yaml
4. **Update regularly** - run `git pull` to get security fixes
5. **Test in Downloads folder** - don't test with real malware!

---

## 🆘 Getting Help

### Check Documentation
- **Main README**: Overview and features
- **INSTALLATION.md**: This file (setup instructions)
- **NOTIFICATION_SETUP.md**: Detailed notification configuration
- **NOTIFICATION_FIX_SUMMARY.md**: Troubleshooting guide

### Common Issues
Most problems are due to:
1. Missing config.yaml (copy from config.yaml.example)
2. Wrong credentials in config.yaml
3. Virtual environment not activated
4. Missing dependencies (run `pip install -r requirements.txt`)

### Still Stuck?
- Check GitHub Issues: https://github.com/fahadkhan91/agentic-security-system/issues
- Review troubleshooting section above
- Make sure all dependencies are installed
- Try running test_notifications.py to isolate the issue

---

## 📊 System Status Check

Run this to verify everything is working:

```bash
#!/bin/bash
echo "🔍 Checking Agentic Security System..."
echo ""

# Check Python
python3 --version && echo "✅ Python installed" || echo "❌ Python not found"

# Check pip
pip3 --version && echo "✅ pip installed" || echo "❌ pip not found"

# Check config
[ -f config.yaml ] && echo "✅ config.yaml exists" || echo "⚠️  config.yaml not found (copy from config.yaml.example)"

# Check dependencies
python3 -c "import streamlit; import yaml; import watchdog" 2>/dev/null && echo "✅ Dependencies installed" || echo "❌ Run: pip install -r requirements.txt"

echo ""
echo "🚀 Ready to run! Execute: python3 -m streamlit run dashboard.py"
```

Save this as `check_system.sh`, make it executable (`chmod +x check_system.sh`), and run it (`./check_system.sh`).

---

## ✅ Installation Complete!

If you've made it here, your Agentic AI Security System should be ready to go!

**Next Steps:**
1. Start the dashboard: `python3 -m streamlit run dashboard.py`
2. Open http://localhost:8501 in your browser
3. Click "Start Monitoring"
4. Enable notifications in the sidebar
5. Test by creating a file: `cd ~/Downloads && echo "test" > virus.exe`

**Enjoy your AI-powered security monitoring system! 🛡️**

---

**Version:** 1.1
**Last Updated:** October 2025
**Repository:** https://github.com/fahadkhan91/agentic-security-system
**License:** MIT (or your preferred license)
