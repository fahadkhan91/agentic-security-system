# Security & Privacy

## 🔒 Your Credentials Are Safe

This document explains how your sensitive information is protected in this project.

---

## 🛡️ What's Protected

### Files That Contain Your Credentials (NOT on GitHub)

| File | Contents | Protected? | Location |
|------|----------|-----------|----------|
| **config.yaml** | Your real email, password, phone, API keys | ✅ **YES** | Only on your machine |

**How it's protected:**
- Listed in `.gitignore`
- Never committed to git
- Never pushed to GitHub
- Never visible to anyone else

### Files That Are Safe to Share (ON GitHub)

| File | Contents | Safe to Share? |
|------|----------|----------------|
| **config.yaml.example** | Template with placeholders like "your-email@gmail.com" | ✅ YES |
| **Source code** (.py files) | Application logic, no secrets | ✅ YES |
| **Documentation** (.md files) | Instructions and guides | ✅ YES |

---

## 🔍 Verification

### Check What's in Git:

```bash
# List all files tracked by git
git ls-files | grep config

# Output should ONLY show:
# config.yaml.example

# Your config.yaml should NOT appear!
```

### Verify .gitignore is Working:

```bash
# This command checks if config.yaml is ignored
git check-ignore -v config.yaml

# Output should show:
# .gitignore:45:config.yaml    config.yaml
# This means it's PROTECTED!
```

### Check What's on GitHub:

Visit your repository:
https://github.com/fahadkhan91/agentic-security-system

**You will see:**
- ✅ config.yaml.example (with dummy data)
- ❌ config.yaml (NOT there - your credentials are safe!)

---

## 📝 What Others See vs What You Have

### On GitHub (Public):

**config.yaml.example:**
```yaml
email:
  enabled: false
  from: "your-email@gmail.com"          # Placeholder
  to: "recipient@example.com"           # Placeholder
  password: "your-app-password-here"    # Placeholder

whatsapp:
  enabled: false
  callmebot:
    phone: "+1234567890"                # Placeholder
    apikey: "your-api-key-here"         # Placeholder
```

### On Your Machine (Private):

**config.yaml:** (example structure, not your actual file)
```yaml
email:
  enabled: true
  from: "YOUR_REAL_EMAIL@gmail.com"     # ← Your actual email
  to: "RECIPIENT@example.com"           # ← Your actual recipient
  password: "abcd efgh ijkl mnop"       # ← Your actual app password

whatsapp:
  enabled: true
  callmebot:
    phone: "+966XXXXXXXXX"              # ← Your actual phone
    apikey: "123456"                    # ← Your actual API key
```

**This never leaves your machine!**

---

## 🚨 Important Security Notes

### 1. Gmail App Password vs Regular Password

**What you should use:**
- ✅ Gmail **App Password** (16 characters, generated from Google)
- ❌ NOT your regular Gmail login password

**Why?**
- App passwords are specific to one application
- Can be revoked without changing your main password
- More secure for automated systems

**How to get one:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (required)
3. Go to https://myaccount.google.com/apppasswords
4. Generate a password for "Mail"
5. Use that 16-character password in config.yaml

### 2. CallMeBot API Key

**What it is:**
- A 6-digit number (like "123456")
- Linked to your WhatsApp number
- Free service, no credit card needed

**Security:**
- Can only send messages to YOUR phone number
- Cannot access your WhatsApp messages or contacts
- Cannot be used to compromise your account

### 3. Config File Best Practices

**DO:**
- ✅ Keep config.yaml on your machine only
- ✅ Use strong, unique passwords
- ✅ Use App Passwords for email (not main password)
- ✅ Regularly update passwords
- ✅ Back up config.yaml to a secure location (USB, encrypted drive)

**DON'T:**
- ❌ Commit config.yaml to git
- ❌ Share config.yaml in emails or chat
- ❌ Upload config.yaml to cloud services
- ❌ Post screenshots of config.yaml
- ❌ Use your main Gmail password

---

## 🔐 How .gitignore Protects You

### What is .gitignore?

It's a file that tells git which files to NEVER track or upload.

### Our .gitignore includes:

```
# Sensitive data (keep your actual config private!)
# Note: config.yaml contains credentials - use config.yaml.example as template
config.yaml

# Python cache
__pycache__/
*.pyc

# Logs
*.log
logs/
```

### This means:

1. Even if you run `git add .` (add everything), config.yaml is skipped
2. Even if you try `git add config.yaml`, it will be ignored
3. It's impossible to accidentally push your credentials

### Test it yourself:

```bash
# Try to add config.yaml
git add config.yaml

# Check status
git status

# You'll see: "nothing to commit, working tree clean"
# config.yaml is NOT staged!
```

---

## 🌐 What Information Is Public on GitHub?

### Public Information (Intentional):

- ✅ Source code (.py files)
- ✅ Documentation (.md files)
- ✅ Configuration template (config.yaml.example)
- ✅ Dependencies list (requirements.txt)

### Private Information (Protected):

- ❌ Your email credentials
- ❌ Your WhatsApp credentials
- ❌ Your actual config.yaml
- ❌ Any passwords or API keys

### Why source code is public:

- Shows how the system works
- Allows others to learn and improve
- No secrets in the code itself
- Educational and transparent

---

## 🔄 If You Fork or Clone

### When someone clones your repository:

```bash
git clone https://github.com/fahadkhan91/agentic-security-system.git
```

**They get:**
- ✅ All source code
- ✅ config.yaml.example (template)
- ✅ Documentation

**They DON'T get:**
- ❌ Your config.yaml
- ❌ Your credentials
- ❌ Your passwords

**They must:**
1. Create their own config.yaml from the example
2. Add their own email credentials
3. Add their own WhatsApp credentials
4. Cannot use your credentials (they don't have them!)

---

## 🛠️ Credential Management Best Practices

### 1. Email (Gmail App Password)

**Security Level:** High
- Generated by Google
- Can be revoked anytime at https://myaccount.google.com/apppasswords
- Specific to one app
- If compromised, revoke and generate new one

### 2. WhatsApp (CallMeBot)

**Security Level:** Medium
- Only sends to your number
- Cannot receive messages
- Cannot access your account
- Free and no credit card required

### 3. Config File Storage

**Recommended:**
- Keep on local machine only
- Back up to encrypted USB drive
- Use file permissions: `chmod 600 config.yaml` (Linux/Mac)
- Never email or message to anyone

**Not Recommended:**
- Public cloud storage (Google Drive, Dropbox)
- Shared network drives
- Email attachments
- Chat apps (WhatsApp, Telegram, etc.)

---

## 🚨 What to Do If Credentials Are Compromised

### If Your Gmail App Password Leaks:

1. Go to https://myaccount.google.com/apppasswords
2. Revoke the compromised app password
3. Generate a new one
4. Update config.yaml with new password
5. Restart the application

**Your main Gmail account is still safe!**

### If Your WhatsApp API Key Leaks:

**CallMeBot:**
1. Message CallMeBot: "I want to reset my API key"
2. They will provide a new key
3. Update config.yaml
4. Old key becomes invalid

**Note:** The leaked key could only send messages to YOUR phone anyway.

---

## ✅ Security Checklist

Before sharing or uploading anything, verify:

- [ ] config.yaml is in .gitignore ✅
- [ ] config.yaml is NOT in `git ls-files` output ✅
- [ ] Only config.yaml.example is tracked by git ✅
- [ ] Using Gmail App Password (not main password) ✅
- [ ] config.yaml has correct file permissions (600 on Linux/Mac) ✅
- [ ] No passwords in any .py files ✅
- [ ] No passwords in commit messages ✅
- [ ] Repository is public but credentials are private ✅

---

## 📚 Additional Resources

### Git Security:
- https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure

### Gmail Security:
- https://support.google.com/accounts/answer/185833 (App Passwords)
- https://support.google.com/accounts/answer/1064203 (2-Step Verification)

### General Best Practices:
- Use password managers (Bitwarden, 1Password, KeePass)
- Enable 2FA wherever possible
- Use unique passwords for each service
- Regularly audit app permissions

---

## 🤝 Contributing

If you're contributing to this project:

1. **NEVER** commit real credentials
2. **ALWAYS** use config.yaml.example for examples
3. **TEST** with your own credentials locally
4. **VERIFY** .gitignore is working before committing

---

## 📞 Security Concerns?

If you believe there's a security issue:

1. **DO NOT** create a public GitHub issue
2. **DO** contact the repository owner privately
3. **DO** review the code yourself (it's open source)
4. **DO** audit what's in .gitignore

---

## ✅ Summary

**Your credentials are safe because:**

1. ✅ config.yaml is in .gitignore
2. ✅ Only config.yaml.example (with fake data) is on GitHub
3. ✅ Git refuses to track config.yaml
4. ✅ Even if you try to add it, it will be ignored
5. ✅ Your actual passwords never leave your machine

**You can safely:**
- Share the GitHub repository link
- Let others clone your code
- Contribute to the project
- Learn from the source code

**Your email password, WhatsApp API key, and all credentials remain private!**

---

**Last Updated:** October 2025
**Repository:** https://github.com/fahadkhan91/agentic-security-system
**Status:** 🔒 Secure
