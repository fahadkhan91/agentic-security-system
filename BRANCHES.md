# Branch Strategy & Version Guide

> Understanding the different branches and which one to use

---

## 🌳 Branch Overview

This project uses multiple branches to keep stable code separate from experimental features.

### Current Branches

| Branch | Version | Status | Use For |
|--------|---------|--------|---------|
| **main** | v1.1 | ✅ **STABLE** | Production, demos, presentations |
| **feature/network-monitoring** | v1.2-dev | 🧪 **EXPERIMENTAL** | Testing new network features |

---

## 📌 main Branch (v1.1 - Stable)

**Status:** ✅ Production Ready

**What it includes:**
- ✅ File monitoring (Downloads, Desktop, Documents)
- ✅ Signature-based malware detection
- ✅ Heuristic analysis (extensions, keywords, patterns)
- ✅ Multi-channel notifications (Email, WhatsApp, Desktop)
- ✅ Web dashboard with real-time updates
- ✅ CLI monitoring interface
- ✅ Complete documentation

**Use this branch if:**
- You want a working, tested system
- You're demoing to others
- You need reliability
- You're presenting at a hackathon
- You're running it in production

**How to use:**
```bash
# Switch to stable branch
git checkout main

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python3 -m streamlit run dashboard.py

# Or run CLI
python3 main_simple.py
```

**Last stable commit:** 6f13037 (Security documentation)

---

## 🧪 feature/network-monitoring Branch (v1.2-dev - Experimental)

**Status:** 🧪 Experimental / Development

**What it adds (in addition to v1.1):**
- ➕ Network connection monitoring
- ➕ IP blacklist from local SRX server
- ➕ Real-time connection threat detection
- ➕ Process identification for suspicious connections
- ➕ Threat intelligence integration (SRX feed)
- ➕ Connection statistics and reporting
- ➕ Comprehensive feature roadmap (ROADMAP.md)

**Use this branch if:**
- You want to test network monitoring
- You have a local SRX server with threat feed
- You're developing new features
- You want to see what's coming next
- You're comfortable troubleshooting

**How to use:**
```bash
# Switch to experimental branch
git checkout feature/network-monitoring

# Install NEW dependencies (includes psutil)
pip install -r requirements.txt

# Configure network monitoring
nano config.yaml  # Set network_monitoring.enabled: true

# Test network monitoring
python3 test_network_monitor.py

# Run dashboard (v1.1 features still work)
python3 -m streamlit run dashboard.py
```

**Latest commit:** 353e109 (Network monitoring)

---

## 🔄 Switching Between Branches

### From Stable to Experimental

```bash
# Save any changes first
git stash  # Optional: if you have uncommitted changes

# Switch to experimental branch
git checkout feature/network-monitoring

# Update dependencies (new: psutil)
pip install -r requirements.txt

# Check what's new
git log main..feature/network-monitoring --oneline
```

### From Experimental Back to Stable

```bash
# Switch back to stable
git checkout main

# Dependencies are same as before
pip install -r requirements.txt

# Everything works as before!
python3 -m streamlit run dashboard.py
```

---

## 📊 Feature Comparison

| Feature | main (v1.1) | feature/network-monitoring (v1.2-dev) |
|---------|-------------|---------------------------------------|
| File monitoring | ✅ Yes | ✅ Yes |
| Malware detection | ✅ Yes | ✅ Yes |
| Email notifications | ✅ Yes | ✅ Yes |
| WhatsApp notifications | ✅ Yes | ✅ Yes |
| Desktop notifications | ✅ Yes | ✅ Yes |
| Web dashboard | ✅ Yes | ✅ Yes |
| CLI interface | ✅ Yes | ✅ Yes |
| **Network monitoring** | ❌ No | ✅ **Yes** |
| **IP blacklist (SRX)** | ❌ No | ✅ **Yes** |
| **Connection tracking** | ❌ No | ✅ **Yes** |
| **Process identification** | ❌ No | ✅ **Yes** |
| **Threat intel feeds** | ❌ No | 🟡 **Partial** |
| **Feature roadmap** | ❌ No | ✅ **Yes** (ROADMAP.md) |

---

## 🚀 When Will Features Merge to main?

The experimental features in `feature/network-monitoring` will be merged to `main` when:

- ✅ All features are thoroughly tested
- ✅ No bugs or issues found
- ✅ Documentation is complete
- ✅ Dashboard integration is finished
- ✅ User feedback is positive
- ✅ Performance is acceptable

**Estimated timeline:** 2-3 weeks of testing

---

## 🧪 Testing the Experimental Branch

### Prerequisites
1. Local SRX server running with threat feed at: `http://localhost/srx/custom-feed.txt`
2. psutil installed: `pip install psutil`
3. Network monitoring enabled in config.yaml

### Testing Steps

**Step 1: Switch to experimental branch**
```bash
git checkout feature/network-monitoring
pip install -r requirements.txt
```

**Step 2: Configure network monitoring**
```bash
cp config.yaml.example config.yaml  # If you don't have config.yaml
nano config.yaml
```

Set in config.yaml:
```yaml
network_monitoring:
  enabled: true
  local_feed_url: "http://localhost/srx/custom-feed.txt"
```

**Step 3: Test SRX feed connection**
```bash
# Verify your SRX feed is accessible
curl http://localhost/srx/custom-feed.txt

# Should return list of IPs
```

**Step 4: Run network monitoring test**
```bash
python3 test_network_monitor.py
```

**Expected output:**
```
📡 Testing SRX Threat Feed...
✅ Successfully loaded X IPs from SRX server

🔍 Testing Connection Monitoring...
📊 Statistics:
  Total connections checked: X
  Unique IPs seen: X
  Blacklisted IPs: X
  Malicious connections: 0 or more

✅ No malicious connections detected
(or)
🚨 Malicious Connections Detected: ...
```

**Step 5: Test with current system**
```bash
# File monitoring still works
python3 main_simple.py

# Dashboard still works
python3 -m streamlit run dashboard.py

# Notifications still work
python3 test_notifications.py
```

---

## 🐛 Reporting Issues

### For Stable Branch (main)
If you find issues in the stable v1.1:
1. Verify you're on main branch: `git branch --show-current`
2. Create GitHub issue with label: `bug`
3. Include: Steps to reproduce, expected vs actual behavior

### For Experimental Branch (feature/network-monitoring)
If you find issues in the experimental v1.2-dev:
1. Verify you're on feature branch: `git branch --show-current`
2. Create GitHub issue with label: `enhancement` or `experimental`
3. Include: Feature being tested, configuration, logs

---

## 📝 Development Workflow

### For Contributors

**Working on existing features (main branch):**
```bash
git checkout main
# Make changes
git add .
git commit -m "Fix: ..."
git push origin main
```

**Working on new features (feature branch):**
```bash
git checkout feature/network-monitoring
# Make changes
git add .
git commit -m "Feature: ..."
git push origin feature/network-monitoring
```

**Creating your own feature branch:**
```bash
git checkout main  # Start from stable
git checkout -b feature/my-new-feature
# Develop your feature
git push -u origin feature/my-new-feature
```

---

## 🔐 Security & Stability

### main Branch Protection
- No experimental features
- Thoroughly tested code only
- Breaking changes require major version bump
- Always production-ready

### Experimental Branch Rules
- Can contain breaking changes
- May have bugs
- Documentation may be incomplete
- Test before using in production
- Feedback welcome

---

## 📚 Which Branch Should I Use?

### Use **main** if you:
- ✅ Want a reliable, working system
- ✅ Are presenting or demoing
- ✅ Need email/WhatsApp/desktop notifications
- ✅ Want file monitoring and malware detection
- ✅ Don't need network monitoring yet
- ✅ Want maximum stability

### Use **feature/network-monitoring** if you:
- 🧪 Have a local SRX server with threat feed
- 🧪 Want to test network connection monitoring
- 🧪 Need IP blacklist checking
- 🧪 Want to see upcoming features
- 🧪 Are comfortable with experimental code
- 🧪 Can help test and provide feedback

---

## 🎯 Quick Commands

```bash
# Check current branch
git branch --show-current

# List all branches
git branch -a

# Switch to stable
git checkout main

# Switch to experimental
git checkout feature/network-monitoring

# Update to latest
git pull

# See what changed between branches
git diff main..feature/network-monitoring

# See commit history
git log --oneline --graph --all
```

---

## 📖 Related Documentation

- **README.md** - Main project documentation
- **INSTALLATION.md** - Setup instructions
- **SECURITY.md** - Credential protection
- **NOTIFICATION_SETUP.md** - Email/WhatsApp configuration
- **ROADMAP.md** - Future features (in feature/network-monitoring branch)

---

## ❓ FAQ

**Q: Will experimental features break my current setup?**
A: No! The main branch is completely separate. You can switch back anytime.

**Q: Can I use both branches?**
A: Not simultaneously, but you can switch between them using `git checkout`.

**Q: Which config.yaml do I need?**
A: Your config.yaml works on both branches. The experimental branch just has additional (optional) settings.

**Q: Do I need to reinstall dependencies when switching?**
A: When switching TO feature/network-monitoring, run `pip install -r requirements.txt` to get psutil.
When switching back to main, dependencies are the same as before.

**Q: How do I know which branch I'm on?**
A: Run `git branch --show-current` or look at your terminal prompt (if configured).

**Q: Can I contribute to the experimental branch?**
A: Yes! Test it, report bugs, suggest improvements via GitHub issues.

---

## 🎉 Summary

- **main** = Your working, stable v1.1 ✅
- **feature/network-monitoring** = New network features to test 🧪
- Both branches are safe and independent
- Easy to switch between them
- Main branch is protected and always stable

**Recommendation:** Stick with **main** for daily use, switch to **feature/network-monitoring** when you want to test network monitoring with your SRX feed.

---

**Last Updated:** October 2025
**Current Stable Version:** v1.1 (main branch)
**Current Dev Version:** v1.2-dev (feature/network-monitoring branch)
**Repository:** https://github.com/fahadkhan91/agentic-security-system
