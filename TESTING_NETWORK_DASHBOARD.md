# Testing Network Monitoring Dashboard

> Quick guide to test the new network monitoring integration

---

## ✅ What's New

The dashboard now includes:
- 🌐 **Network Monitoring Section** - Shows connection statistics
- 🚨 **Malicious Connection Alerts** - Red alert boxes for blacklist hits
- 📊 **Live Statistics** - Connections checked, blocked, blacklist size, unique IPs
- 🔔 **Automatic Notifications** - Email/WhatsApp/Desktop alerts for network threats
- 🔗 **SRX Feed Status** - Shows if your SRX feed is connected

---

## 🚀 How to Test

### **Step 1: Make Sure You're on the Feature Branch**

```bash
cd /home/fahad/agentic_security_system
git branch --show-current
# Should show: feature/network-monitoring
```

If not:
```bash
git checkout feature/network-monitoring
```

---

### **Step 2: Verify config.yaml Has Network Monitoring Enabled**

```bash
cat config.yaml | grep -A 5 "network_monitoring"
```

Should show:
```yaml
network_monitoring:
  enabled: true  # ← Must be true
  local_feed_url: "http://localhost/srx/custom-feed.txt"
```

If `enabled: false`, change it to `true`:
```bash
nano config.yaml
# Find network_monitoring section
# Change enabled: false to enabled: true
# Save: Ctrl+O, Enter, Ctrl+X
```

---

### **Step 3: Start the Dashboard**

```bash
python3.11 -m streamlit run dashboard.py
```

**Expected:**
- Dashboard opens at http://localhost:8501
- Browser should open automatically

---

### **Step 4: Start Monitoring**

In the dashboard:
1. Click **"🚀 Start Monitoring"** in the sidebar (left side)
2. Wait a moment for initialization

**You should see:**
- File monitoring section (existing features)
- Statistics showing files scanned
- **NEW: Network Monitoring section** (below file monitoring)

---

### **Step 5: Check Network Monitoring Section**

Scroll down past the file monitoring section.

**You should see:**

```
🌐 Network Monitoring
━━━━━━━━━━━━━━━━━━━

🔍 Connections Checked    🚨 Blocked    📊 Blacklist Size    🌍 Unique IPs
         X                    0                4                  X

✅ No malicious connections detected

🔗 SRX Feed: Connected (4 IPs loaded)
```

**What this means:**
- ✅ **"Connected (4 IPs loaded)"** = Your SRX feed is working!
- ✅ **Connections Checked** = Dashboard is monitoring
- ✅ **Blacklist Size: 4** = Your 4 IPs from SRX feed are loaded

---

### **Step 6: Test Notifications (Optional)**

If you have notifications enabled and want to test:

1. Make sure **"Enable Notifications"** is checked in sidebar
2. Dashboard will automatically send Email/WhatsApp/Desktop alerts if it detects a connection to a blacklisted IP

---

## 📊 What You Should See

### **Normal Operation (No Threats)**

```
🌐 Network Monitoring

🔍 Connections Checked: 25
🚨 Blocked: 0
📊 Blacklist Size: 4
🌍 Unique IPs: 10

✅ No malicious connections detected

🔗 SRX Feed: Connected (4 IPs loaded)
```

### **If Malicious Connection Detected**

```
🌐 Network Monitoring

🔍 Connections Checked: 30
🚨 Blocked: 1  ← Increased!
📊 Blacklist Size: 4
🌍 Unique IPs: 12

🚨 Malicious Connections Detected

┌─────────────────────────────────────────┐
│ ⚠️ Connection to Blacklisted IP         │
│                                          │
│ IP: 1.1.1.1:443                         │
│ Process: chrome (PID: 12345)            │
│ Time: 15:30:25                          │
│ Threat Score: 85/100                    │
└─────────────────────────────────────────┘
```

**If this happens:**
- ✅ Network monitoring is working perfectly!
- ✅ It detected a connection to a blacklisted IP
- ✅ You'll receive Email/WhatsApp/Desktop notification (if enabled)

---

## ✅ Success Indicators

| Indicator | What It Means |
|-----------|---------------|
| **Network Monitoring section appears** | ✅ Integration successful |
| **"SRX Feed: Connected (4 IPs loaded)"** | ✅ SRX feed is working |
| **Connections Checked > 0** | ✅ Monitoring active connections |
| **Blacklist Size: 4** | ✅ IPs loaded from your SRX feed |
| **Statistics update when you refresh** | ✅ Real-time monitoring working |

---

## 🐛 Troubleshooting

### **Problem: Network Monitoring section doesn't appear**

**Solution:**
```bash
# 1. Check if network monitoring is enabled
cat config.yaml | grep "network_monitoring:" -A 2

# Should show:
# network_monitoring:
#   enabled: true

# 2. If false, edit and change to true
nano config.yaml

# 3. Restart dashboard
# Press Ctrl+C in terminal
# Then: python3.11 -m streamlit run dashboard.py
```

---

### **Problem: "SRX Feed: Not loaded"**

**Solution:**
```bash
# 1. Test SRX feed directly
curl http://localhost/srx/custom-feed.txt

# 2. Should show IPs like:
# 1.1.1.1/32
# 10.1.1.1/32
# etc.

# 3. If curl fails, check:
#    - Is SRX server running?
#    - Is URL correct in config.yaml?
```

---

### **Problem: "Blacklist Size: 0"**

**Means:** SRX feed couldn't be loaded

**Solution:**
```bash
# Check connection
curl http://localhost/srx/custom-feed.txt

# Check config
cat config.yaml | grep "local_feed_url"

# Restart dashboard
```

---

## 🎯 What to Test

### ✅ **Basic Functionality**
- [ ] Dashboard opens successfully
- [ ] Network Monitoring section appears
- [ ] SRX feed shows "Connected (4 IPs loaded)"
- [ ] Statistics show numbers > 0
- [ ] File monitoring still works
- [ ] Existing features unchanged

### ✅ **Real-time Updates**
- [ ] Statistics update when dashboard refreshes
- [ ] Connections Checked number increases
- [ ] Unique IPs count updates

### ✅ **Integration**
- [ ] File monitoring and network monitoring both visible
- [ ] Both sections update independently
- [ ] No errors in dashboard
- [ ] Dashboard performance is good

---

## 📸 Expected Dashboard Layout

```
┌─────────────────────────────────────────┐
│   🛡️ Agentic AI Security Monitor        │
│   Multi-Agent Threat Detection          │
└─────────────────────────────────────────┘

🤖 Agent Status
[File Watcher] [Scanner] [Coordinator] [Alert]

📊 Statistics
[Files Scanned] [Threats] [Critical] [Alerts]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Activity Log          🚨 Recent Threats
[Recent files...]        [Threats if any...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Network Monitoring    ← NEW SECTION!

[Connections] [Blocked] [Blacklist] [IPs]

✅ No malicious connections detected
🔗 SRX Feed: Connected (4 IPs loaded)
```

---

## 🔄 Testing Workflow

```bash
# 1. Start dashboard
python3.11 -m streamlit run dashboard.py

# 2. In dashboard:
#    - Click "Start Monitoring"
#    - Check "Enable Notifications" (if you want alerts)

# 3. Verify:
#    ✅ File monitoring section works
#    ✅ Network monitoring section appears
#    ✅ SRX feed connected
#    ✅ Statistics show data

# 4. Let it run for a few minutes
#    - Watch statistics update
#    - Check for any errors

# 5. Stop:
#    - Click "Stop Monitoring"
#    - Or press Ctrl+C in terminal
```

---

## 💡 Tips

1. **Auto-refresh is enabled by default** - The dashboard updates every 3 seconds
2. **Network monitoring runs automatically** - No need to do anything special
3. **Notifications are automatic** - If blacklisted IP detected and notifications enabled
4. **Safe to test** - Won't break existing functionality
5. **Can switch back to main branch anytime** - `git checkout main`

---

## ✅ Test Complete Checklist

After testing, confirm:

- [ ] Dashboard opens without errors
- [ ] Network Monitoring section visible
- [ ] SRX feed shows "Connected (4 IPs loaded)"
- [ ] Statistics are updating
- [ ] File monitoring still works
- [ ] Can start/stop monitoring
- [ ] No console errors
- [ ] Dashboard performance is acceptable

---

## 📝 Report Results

After testing, let me know:

1. **Did the network monitoring section appear?** (Yes/No)
2. **SRX feed status?** (Connected with X IPs / Not loaded)
3. **Any errors?** (Paste error messages if any)
4. **Performance?** (Fast / Slow / Acceptable)
5. **Malicious connections detected?** (Number, if any)
6. **Overall impression?** (Working well / Issues / Suggestions)

---

## 🎉 Success Criteria

**Test PASSED if:**
- ✅ Network section appears
- ✅ SRX feed connected
- ✅ Statistics update
- ✅ No errors
- ✅ File monitoring still works

**Test FAILED if:**
- ❌ Dashboard won't start
- ❌ Network section missing
- ❌ Errors in console
- ❌ SRX feed not loading
- ❌ Existing features broken

---

**Ready to test? Run:** `python3.11 -m streamlit run dashboard.py`

**Questions? Check:** BRANCHES.md for branch info

**Need help? Switch back to stable:** `git checkout main`
