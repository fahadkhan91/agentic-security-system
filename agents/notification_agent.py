"""
Notification Agent
Sends alerts via Email, WhatsApp, and Desktop notifications.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from .base_agent import BaseSecurityAgent

# Try to import optional dependencies
try:
    from plyer import notification as desktop_notify
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class NotificationAgent(BaseSecurityAgent):
    """Agent responsible for sending notifications via multiple channels."""

    def __init__(self, config=None):
        """
        Initialize notification agent.

        Args:
            config: Dictionary with notification settings
        """
        super().__init__("NotificationAgent", "alert")

        # Default configuration
        self.config = config or {}

        # Email settings
        self.email_enabled = self.config.get('email_enabled', False)
        self.email_from = self.config.get('email_from', '')
        self.email_to = self.config.get('email_to', '')
        self.email_password = self.config.get('email_password', '')
        self.smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.config.get('smtp_port', 587)

        # WhatsApp settings (via Twilio or CallMeBot)
        self.whatsapp_enabled = self.config.get('whatsapp_enabled', False)
        self.whatsapp_method = self.config.get('whatsapp_method', 'callmebot')  # 'callmebot' or 'twilio'

        # CallMeBot settings (free, no API key needed)
        self.callmebot_phone = self.config.get('callmebot_phone', '')  # Format: +1234567890
        self.callmebot_apikey = self.config.get('callmebot_apikey', '')  # Get from wa.me/+34644328808

        # Twilio settings (requires account)
        self.twilio_account_sid = self.config.get('twilio_account_sid', '')
        self.twilio_auth_token = self.config.get('twilio_auth_token', '')
        self.twilio_from = self.config.get('twilio_from', '')  # Your Twilio WhatsApp number
        self.twilio_to = self.config.get('twilio_to', '')  # Recipient WhatsApp number

        # Desktop notification settings
        self.desktop_enabled = self.config.get('desktop_enabled', True)

        # Notification history
        self.notifications_sent = {
            'email': 0,
            'whatsapp': 0,
            'desktop': 0
        }

    def run(self):
        """Notification agent runs on-demand, not continuous."""
        pass

    def send_threat_alert(self, threat_info):
        """
        Send threat alert via all enabled channels.

        Args:
            threat_info: Dictionary with threat details
        """
        urgency = threat_info.get('urgency', 'LOW')
        filename = threat_info.get('filename', 'Unknown')
        threat_score = threat_info.get('threat_score', 0)
        reasons = threat_info.get('reasons', [])

        # Only send notifications for medium+ threats
        if threat_score < 50:
            self.log_action("SKIP_NOTIFICATION", f"Threat score too low ({threat_score}) for {filename}")
            return

        # Prepare message
        message = self.format_alert_message(threat_info)
        subject = f"🚨 {urgency} THREAT DETECTED: {filename}"

        # Send via all enabled channels
        results = {
            'email': False,
            'whatsapp': False,
            'desktop': False
        }

        if self.desktop_enabled and PLYER_AVAILABLE:
            results['desktop'] = self.send_desktop_notification(subject, message, urgency)

        if self.email_enabled:
            results['email'] = self.send_email_notification(subject, message)

        if self.whatsapp_enabled:
            results['whatsapp'] = self.send_whatsapp_notification(message)

        self.log_action(
            "NOTIFICATIONS_SENT",
            f"Sent alerts for {filename} - Email: {results['email']}, "
            f"WhatsApp: {results['whatsapp']}, Desktop: {results['desktop']}"
        )

        return results

    def format_alert_message(self, threat_info):
        """Format threat information into a readable message."""
        urgency = threat_info.get('urgency', 'UNKNOWN')
        filename = threat_info.get('filename', 'Unknown')
        threat_score = threat_info.get('threat_score', 0)
        reasons = threat_info.get('reasons', [])
        timestamp = threat_info.get('timestamp', datetime.now())

        message = f"""
🚨 SECURITY ALERT 🚨

Threat Level: {urgency}
File: {filename}
Threat Score: {threat_score}/100
Detected: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Analysis:
{chr(10).join(['• ' + r for r in reasons]) if reasons else '• No specific reasons listed'}

Action: File has been flagged for quarantine.

---
Agentic AI Security System
Multi-Agent Threat Detection
        """.strip()

        return message

    def send_email_notification(self, subject, message):
        """
        Send email notification.

        Args:
            subject: Email subject
            message: Email body

        Returns:
            bool: True if sent successfully
        """
        if not self.email_enabled:
            return False

        if not all([self.email_from, self.email_to, self.email_password]):
            self.log_action("EMAIL_ERROR", "Missing email configuration")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(message, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_from, self.email_password)

            # Send email
            server.send_message(msg)
            server.quit()

            self.notifications_sent['email'] += 1
            self.log_action("EMAIL_SENT", f"Alert sent to {self.email_to}")
            return True

        except Exception as e:
            self.log_action("EMAIL_ERROR", f"Failed to send email: {str(e)}")
            return False

    def send_whatsapp_notification(self, message):
        """
        Send WhatsApp notification.

        Args:
            message: Message to send

        Returns:
            bool: True if sent successfully
        """
        if not self.whatsapp_enabled or not REQUESTS_AVAILABLE:
            return False

        if self.whatsapp_method == 'callmebot':
            return self._send_whatsapp_callmebot(message)
        elif self.whatsapp_method == 'twilio':
            return self._send_whatsapp_twilio(message)
        else:
            self.log_action("WHATSAPP_ERROR", f"Unknown WhatsApp method: {self.whatsapp_method}")
            return False

    def _send_whatsapp_callmebot(self, message):
        """
        Send WhatsApp via CallMeBot (free service).

        Setup:
        1. Add phone number +34 644 32 88 08 to contacts as "CallMeBot"
        2. Send "I allow callmebot to send me messages" to this contact via WhatsApp
        3. You'll receive your API key

        Args:
            message: Message to send

        Returns:
            bool: True if sent successfully
        """
        if not all([self.callmebot_phone, self.callmebot_apikey]):
            self.log_action("WHATSAPP_ERROR", "Missing CallMeBot configuration")
            return False

        try:
            # CallMeBot API endpoint
            url = "https://api.callmebot.com/whatsapp.php"

            # Remove + from phone number if present
            phone = self.callmebot_phone.replace('+', '')

            # Prepare parameters
            params = {
                'phone': phone,
                'text': message,
                'apikey': self.callmebot_apikey
            }

            # Send request
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                self.notifications_sent['whatsapp'] += 1
                self.log_action("WHATSAPP_SENT", f"Alert sent via CallMeBot to {self.callmebot_phone}")
                return True
            else:
                self.log_action("WHATSAPP_ERROR", f"CallMeBot returned status {response.status_code}")
                return False

        except Exception as e:
            self.log_action("WHATSAPP_ERROR", f"Failed to send WhatsApp via CallMeBot: {str(e)}")
            return False

    def _send_whatsapp_twilio(self, message):
        """
        Send WhatsApp via Twilio (requires paid account).

        Setup:
        1. Create Twilio account (https://www.twilio.com/)
        2. Get Account SID and Auth Token
        3. Set up WhatsApp sandbox or get approved number

        Args:
            message: Message to send

        Returns:
            bool: True if sent successfully
        """
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_from, self.twilio_to]):
            self.log_action("WHATSAPP_ERROR", "Missing Twilio configuration")
            return False

        try:
            # Twilio API endpoint
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"

            # Prepare data
            data = {
                'From': f'whatsapp:{self.twilio_from}',
                'To': f'whatsapp:{self.twilio_to}',
                'Body': message
            }

            # Send request with authentication
            response = requests.post(
                url,
                data=data,
                auth=(self.twilio_account_sid, self.twilio_auth_token),
                timeout=10
            )

            if response.status_code in [200, 201]:
                self.notifications_sent['whatsapp'] += 1
                self.log_action("WHATSAPP_SENT", f"Alert sent via Twilio to {self.twilio_to}")
                return True
            else:
                self.log_action("WHATSAPP_ERROR", f"Twilio returned status {response.status_code}")
                return False

        except Exception as e:
            self.log_action("WHATSAPP_ERROR", f"Failed to send WhatsApp via Twilio: {str(e)}")
            return False

    def send_desktop_notification(self, title, message, urgency='MEDIUM'):
        """
        Send desktop notification.

        Args:
            title: Notification title
            message: Notification message
            urgency: Urgency level (for styling)

        Returns:
            bool: True if sent successfully
        """
        if not self.desktop_enabled or not PLYER_AVAILABLE:
            return False

        try:
            # Truncate message for desktop notification
            short_message = message[:200] + "..." if len(message) > 200 else message

            # Choose icon based on urgency
            icon_map = {
                'CRITICAL': '🚨',
                'HIGH': '⚠️',
                'MEDIUM': '⚡',
                'LOW': 'ℹ️'
            }
            icon = icon_map.get(urgency, 'ℹ️')

            # Send notification
            desktop_notify(
                title=f"{icon} {title}",
                message=short_message,
                app_name='Security Monitor',
                timeout=10
            )

            self.notifications_sent['desktop'] += 1
            self.log_action("DESKTOP_NOTIFICATION", f"Desktop alert shown: {title}")
            return True

        except Exception as e:
            self.log_action("DESKTOP_ERROR", f"Failed to send desktop notification: {str(e)}")
            return False

    def get_status(self):
        """Get notification agent status."""
        status = super().get_status()
        status.update({
            'email_enabled': self.email_enabled,
            'whatsapp_enabled': self.whatsapp_enabled,
            'desktop_enabled': self.desktop_enabled,
            'notifications_sent': self.notifications_sent,
            'total_sent': sum(self.notifications_sent.values())
        })
        return status

    def test_notifications(self):
        """
        Test all notification channels.

        Returns:
            dict: Test results for each channel
        """
        test_threat = {
            'urgency': 'MEDIUM',
            'filename': 'test_malware.exe',
            'threat_score': 75,
            'reasons': ['This is a test notification from the security system'],
            'timestamp': datetime.now()
        }

        results = self.send_threat_alert(test_threat)

        return {
            'email': {
                'enabled': self.email_enabled,
                'sent': results.get('email', False),
                'configured': bool(self.email_from and self.email_to and self.email_password)
            },
            'whatsapp': {
                'enabled': self.whatsapp_enabled,
                'sent': results.get('whatsapp', False),
                'method': self.whatsapp_method,
                'configured': self._is_whatsapp_configured()
            },
            'desktop': {
                'enabled': self.desktop_enabled,
                'sent': results.get('desktop', False),
                'available': PLYER_AVAILABLE
            }
        }

    def _is_whatsapp_configured(self):
        """Check if WhatsApp is properly configured."""
        if self.whatsapp_method == 'callmebot':
            return bool(self.callmebot_phone and self.callmebot_apikey)
        elif self.whatsapp_method == 'twilio':
            return bool(all([
                self.twilio_account_sid,
                self.twilio_auth_token,
                self.twilio_from,
                self.twilio_to
            ]))
        return False
