# WhatsApp Setup Tutorial - Step by Step

## 🎯 Goal
Get WhatsApp notifications from your security system in **5 minutes** - completely FREE!

---

## 📱 Method: CallMeBot (FREE - No Credit Card!)

CallMeBot is a **free service** that lets you send WhatsApp messages to yourself. Perfect for hackathon demos!

---

## Step-by-Step Setup

### Step 1: Add CallMeBot to Your Phone Contacts (1 minute)

1. **Open your phone's contacts app**
2. **Create a new contact** with these details:
   - **Name**: `CallMeBot` (or any name you like)
   - **Phone Number**: `+34 644 32 88 08`

3. **Save the contact**

**Important**:
- Include the `+34` country code
- This is CallMeBot's official WhatsApp number
- It's safe - this is a legitimate service used by thousands

---

### Step 2: Send Activation Message via WhatsApp (1 minute)

1. **Open WhatsApp** on your phone

2. **Start a chat** with the contact you just created (CallMeBot)

3. **Send this EXACT message**:
   ```
   I allow callmebot to send me messages
   ```

   **Type it exactly** - including capitalization and spaces!

4. **Wait 5-10 seconds**

5. **You'll receive a reply** from CallMeBot that looks like this:
   ```
   API Activated for +923001234567

   Your APIKEY is 123456

   To send messages use:
   https://api.callmebot.com/whatsapp.php?phone=923001234567&apikey=123456&text=Hello+World
   ```

6. **Copy your API key** (the number after "Your APIKEY is")
   - In the example above, it's `123456`
   - **Your API key will be different!**
   - **Save it somewhere** - you'll need it in Step 3

---

### Step 3: Configure Your Security System (2 minutes)

1. **Open Terminal** and navigate to project:
   ```bash
   cd /home/fahad/agentic_security_system
   ```

2. **Open config.yaml** in a text editor:
   ```bash
   nano config.yaml
   # OR
   gedit config.yaml
   # OR any text editor you prefer
   ```

3. **Find the WhatsApp section** (around line 17):
   ```yaml
   whatsapp:
     enabled: false  # Change this to true
     method: "callmebot"
     callmebot:
       phone: "+1234567890"  # Change to your phone
       apikey: ""  # Put your API key here
   ```

4. **Edit it** to look like this:
   ```yaml
   whatsapp:
     enabled: true  # ← Changed to true
     method: "callmebot"
     callmebot:
       phone: "+923001234567"  # ← YOUR phone number with country code
       apikey: "123456"  # ← YOUR API key from Step 2
   ```

   **Replace with YOUR details**:
   - `+923001234567` → Your actual phone number (with country code!)
   - `123456` → Your actual API key from CallMeBot

5. **Save the file**:
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`
   - In gedit: Click Save

---

### Step 4: Test It! (1 minute)

1. **Run the test script**:
   ```bash
   python3 test_notifications.py
   ```

2. **You should see**:
   ```
   ======================================================================
     NOTIFICATION SYSTEM TEST
   ======================================================================

   📋 Configuration Status:
   ----------------------------------------------------------------------
   📱 WhatsApp Notifications:
      Status: ✓ ENABLED
      Method: callmebot
      Phone: +923001234567
      API Key: ****** (configured)

   🔔 Sending test notifications...
   ----------------------------------------------------------------------

   📊 Results:
   ----------------------------------------------------------------------
      📱 WhatsApp: ✓ SENT to +923001234567
   ----------------------------------------------------------------------

   ✅ Successfully sent 1 notification(s)!

   👀 Check for notifications:
      📱 Check WhatsApp on: +923001234567
   ```

3. **Check your phone!** 📱
   - Open WhatsApp
   - You should see a message from CallMeBot
   - It contains the test threat alert!

---

## 🎉 Success!

If you received the WhatsApp message, **you're all set!**

Now when you run the security system and it detects a threat, you'll get instant WhatsApp alerts!

---

## Common Issues & Solutions

### ❌ Issue 1: "Missing CallMeBot configuration"

**Problem**: API key or phone number not in config.yaml

**Solution**:
1. Make sure `enabled: true` (not `enabled: false`)
2. Check phone number has country code (e.g., `+92`, `+1`, `+44`)
3. Check API key is in quotes: `apikey: "123456"`
4. Make sure YAML spacing is correct (2 spaces for indentation)

**Correct format**:
```yaml
whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"
    apikey: "123456"
```

**Wrong format** (common mistakes):
```yaml
whatsapp:
  enabled: false  # ❌ Should be true
  method: "callmebot"
  callmebot:
    phone: "923001234567"  # ❌ Missing + symbol
    apikey: 123456  # ❌ Should be in quotes
```

---

### ❌ Issue 2: "CallMeBot returned status 401"

**Problem**: Wrong API key or phone number

**Solution**:
1. Go back to WhatsApp
2. Find the message from CallMeBot
3. Copy the API key exactly (just the numbers)
4. Make sure phone number matches exactly
5. Update config.yaml

---

### ❌ Issue 3: No message from CallMeBot after activation

**Problem**: Activation message not recognized

**Solution**:
1. Delete the chat with CallMeBot
2. Start a NEW chat
3. Send EXACTLY: `I allow callmebot to send me messages`
   - Don't add punctuation
   - Don't add emoji
   - Copy-paste if unsure
4. Wait 30 seconds
5. If still nothing, the number might be +34 644 32 88 08 (check official site)

---

### ❌ Issue 4: "requests module not found"

**Problem**: Python requests library not installed

**Solution**:
```bash
pip install requests
# OR
pip install -r requirements.txt
```

---

### ❌ Issue 5: Phone number format confusion

**Problem**: Not sure about country code

**Solution**:
- Pakistan: `+92` followed by your number (remove leading 0)
  - If your number is: 0300-1234567
  - Write as: `+923001234567`
- USA/Canada: `+1` followed by your number
  - If your number is: (555) 123-4567
  - Write as: `+15551234567`
- UK: `+44` followed by your number (remove leading 0)
  - If your number is: 07700 900123
  - Write as: `+447700900123`
- India: `+91` followed by your number
  - If your number is: 98765 43210
  - Write as: `+919876543210`

**Format**: `+[country code][number without leading zero or spaces]`

---

## Full Example with Pakistani Number

If your phone number is **0300-1234567**:

### WhatsApp Activation:
1. Add contact: `+34 644 32 88 08`
2. Send: `I allow callmebot to send me messages`
3. Receive: `Your APIKEY is 789012`

### config.yaml:
```yaml
whatsapp:
  enabled: true
  method: "callmebot"
  callmebot:
    phone: "+923001234567"  # Note: +92 then 300... (no leading 0)
    apikey: "789012"  # Your actual API key
```

---

## Testing with Real Threat Detection

Once WhatsApp is working, test the full system:

### Terminal 1: Start System
```bash
cd /home/fahad/agentic_security_system
streamlit run dashboard.py
```

### In Dashboard:
1. Click "Start Monitoring"

### Terminal 2: Create Threat
```bash
cd ~/Downloads
echo "test" > virus.exe
```

### Result:
- Dashboard shows threat immediately
- **WhatsApp message arrives** 📱
- Desktop notification appears

---

## What the WhatsApp Message Looks Like

You'll receive a message like this:

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

---

## Video Tutorial Alternative

If you prefer watching a video, CallMeBot has official tutorials:
- YouTube: Search "CallMeBot WhatsApp API tutorial"
- Official site: https://www.callmebot.com/blog/free-api-whatsapp-messages/

---

## Important Notes

### Free Limits
- CallMeBot is FREE forever
- No credit card needed
- Unlimited messages (fair use)
- Response time: Usually instant (sometimes 1-2 seconds)

### Privacy
- CallMeBot only sends to YOUR number
- They don't store your messages
- It's safe for demos and personal use

### For Production
If you later want to scale this to production:
- Use Twilio WhatsApp API (paid, more reliable)
- Or WhatsApp Business API (official, requires approval)
- CallMeBot is perfect for demos and personal use!

---

## Alternative: Email Notifications (If WhatsApp Doesn't Work)

If you can't get WhatsApp working, use email instead:

### Gmail Setup (5 minutes):

1. **Enable 2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow steps

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Copy the 16-character password

3. **Update config.yaml**:
   ```yaml
   email:
     enabled: true
     from: "your.email@gmail.com"
     to: "your.email@gmail.com"
     password: "abcd efgh ijkl mnop"  # App password
   ```

4. **Test**:
   ```bash
   python3 test_notifications.py
   ```

---

## Quick Reference Card

**Save this for easy reference:**

```
===========================================
WHATSAPP SETUP QUICK REFERENCE
===========================================

1. Add contact: +34 644 32 88 08
2. Send message: "I allow callmebot to send me messages"
3. Copy API key from reply
4. Edit config.yaml:
   whatsapp:
     enabled: true
     callmebot:
       phone: "+92XXXXXXXXXX"  # Your number
       apikey: "XXXXXX"  # Your API key
5. Test: python3 test_notifications.py
6. Check WhatsApp on your phone!

===========================================
```

---

## Help & Support

If you're still stuck:

1. **Check CallMeBot official site**: https://www.callmebot.com/
2. **Re-read error messages** - they usually tell you what's wrong
3. **Try email notifications** instead (works great too!)
4. **Desktop notifications** always work (no setup needed)

---

## You're Ready! 🎉

Once you see the test message on your phone, you're **100% ready** for the hackathon!

The live WhatsApp notification during your demo will be **extremely impressive** to judges!

Good luck! 🚀📱
