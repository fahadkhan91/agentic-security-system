"""
Network Monitor Agent
Monitors network connections and checks against local and external threat feeds.
"""

import os
import psutil
import requests
import time
from datetime import datetime, timedelta
from .base_agent import BaseSecurityAgent


class NetworkMonitorAgent(BaseSecurityAgent):
    """Agent responsible for monitoring network connections and threat intelligence."""

    def __init__(self, config=None):
        """
        Initialize network monitor agent.

        Args:
            config: Dictionary with network monitoring settings
        """
        super().__init__("NetworkMonitor", "network")

        # Configuration
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)

        # Local threat feed (your SRX server)
        self.local_feed_url = self.config.get('local_feed_url', 'http://localhost/srx/custom-feed.txt')

        # External threat feeds
        self.external_feeds = self.config.get('external_feeds', {})

        # Blacklist and whitelist
        self.ip_blacklist = set()
        self.ip_whitelist = set()

        # Cache for threat intelligence queries
        self.threat_cache = {}
        self.cache_duration = self.config.get('cache_duration', 3600)  # 1 hour

        # Monitoring settings
        self.scan_interval = self.config.get('scan_interval', 5)  # seconds
        self.log_all_connections = self.config.get('log_all_connections', False)

        # Connection history
        self.connections = []
        self.malicious_connections = []

        # Statistics
        self.stats = {
            'total_connections': 0,
            'blocked_connections': 0,
            'unique_ips': set(),
            'last_update': None
        }

        # Load initial blacklist
        self.update_blacklist()

        self.log_action("INIT", "Network monitor agent initialized")

    def run(self):
        """Main monitoring loop."""
        if not self.enabled:
            return

        while True:
            try:
                self.monitor_connections()
                time.sleep(self.scan_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log_action("ERROR", f"Monitoring error: {str(e)}")

    def update_blacklist(self):
        """Update IP blacklist from local and external feeds."""
        self.log_action("UPDATE", "Updating threat feeds...")

        # Load from local SRX feed
        local_ips = self.load_local_feed()
        if local_ips:
            self.ip_blacklist.update(local_ips)
            self.log_action("FEED_UPDATE", f"Loaded {len(local_ips)} IPs from local SRX feed")

        # Load from external feeds (if configured)
        if self.external_feeds.get('abuseipdb_enabled'):
            # External feeds can be added here
            pass

        # Load whitelist
        whitelist_file = self.config.get('whitelist_file')
        if whitelist_file and os.path.exists(whitelist_file):
            with open(whitelist_file, 'r') as f:
                self.ip_whitelist = set(line.strip() for line in f if line.strip())

        self.stats['last_update'] = datetime.now()
        self.log_action("UPDATE", f"Blacklist updated: {len(self.ip_blacklist)} IPs")

    def load_local_feed(self):
        """Load IP blacklist from local SRX server."""
        try:
            response = requests.get(self.local_feed_url, timeout=10)

            if response.status_code == 200:
                # Parse IPs from feed
                ips = set()
                for line in response.text.split('\n'):
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Extract IP (handle various formats)
                    # Format 1: Just IP (e.g., 1.1.1.1)
                    # Format 2: IP/CIDR (e.g., 1.1.1.1/32)
                    # Format 3: IP,description
                    # Format 4: IP	description
                    parts = line.replace('\t', ',').split(',')
                    ip_part = parts[0].strip()

                    # Remove CIDR notation if present (e.g., /32)
                    if '/' in ip_part:
                        ip = ip_part.split('/')[0].strip()
                    else:
                        ip = ip_part

                    # Basic IP validation
                    if self.is_valid_ip(ip):
                        ips.add(ip)

                return ips

            else:
                self.log_action("FEED_ERROR", f"Failed to load local feed: HTTP {response.status_code}")
                return set()

        except requests.exceptions.ConnectionError:
            self.log_action("FEED_ERROR", "Cannot connect to local SRX server")
            return set()
        except Exception as e:
            self.log_action("FEED_ERROR", f"Error loading local feed: {str(e)}")
            return set()

    def is_valid_ip(self, ip_str):
        """Basic IP address validation."""
        try:
            parts = ip_str.split('.')
            if len(parts) != 4:
                return False
            return all(0 <= int(part) <= 255 for part in parts)
        except (ValueError, AttributeError):
            return False

    def monitor_connections(self):
        """Monitor active network connections."""
        try:
            connections = psutil.net_connections(kind='inet')

            for conn in connections:
                # Only monitor established connections
                if conn.status != psutil.CONN_ESTABLISHED:
                    continue

                # Skip if no remote address
                if not conn.raddr:
                    continue

                remote_ip = conn.raddr.ip
                remote_port = conn.raddr.port

                # Skip localhost and private IPs (optional)
                if self.is_private_ip(remote_ip):
                    continue

                # Skip whitelisted IPs
                if remote_ip in self.ip_whitelist:
                    continue

                # Update statistics
                self.stats['total_connections'] += 1
                self.stats['unique_ips'].add(remote_ip)

                # Check against blacklist
                if remote_ip in self.ip_blacklist:
                    self.report_malicious_connection(conn, remote_ip, remote_port)

                # Log all connections if enabled
                elif self.log_all_connections:
                    self.log_connection(conn, remote_ip, remote_port)

        except Exception as e:
            self.log_action("MONITOR_ERROR", f"Error monitoring connections: {str(e)}")

    def is_private_ip(self, ip):
        """Check if IP is private/internal."""
        try:
            parts = [int(x) for x in ip.split('.')]

            # 127.0.0.0/8 (localhost)
            if parts[0] == 127:
                return True

            # 10.0.0.0/8
            if parts[0] == 10:
                return True

            # 172.16.0.0/12
            if parts[0] == 172 and 16 <= parts[1] <= 31:
                return True

            # 192.168.0.0/16
            if parts[0] == 192 and parts[1] == 168:
                return True

            return False

        except Exception:
            return False

    def report_malicious_connection(self, conn, ip, port):
        """Report connection to blacklisted IP."""
        # Get process info
        try:
            process = psutil.Process(conn.pid) if conn.pid else None
            process_name = process.name() if process else "Unknown"
            process_exe = process.exe() if process else "Unknown"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"
            process_exe = "Unknown"

        threat_info = {
            'type': 'MALICIOUS_CONNECTION',
            'urgency': 'HIGH',
            'timestamp': datetime.now(),
            'ip': ip,
            'port': port,
            'protocol': 'TCP',
            'process_name': process_name,
            'process_exe': process_exe,
            'process_pid': conn.pid,
            'local_port': conn.laddr.port if conn.laddr else None,
            'threat_score': 85,
            'reasons': [
                f'Connection to blacklisted IP: {ip}',
                f'Process: {process_name} (PID: {conn.pid})',
                f'Remote port: {port}'
            ]
        }

        # Store in history
        self.malicious_connections.append(threat_info)
        self.stats['blocked_connections'] += 1

        # Log the threat
        self.log_action(
            "THREAT_DETECTED",
            f"Malicious connection: {process_name} → {ip}:{port}"
        )

        return threat_info

    def log_connection(self, conn, ip, port):
        """Log connection details."""
        try:
            process = psutil.Process(conn.pid) if conn.pid else None
            process_name = process.name() if process else "Unknown"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"

        self.log_action(
            "CONNECTION",
            f"{process_name} → {ip}:{port}"
        )

    def get_recent_threats(self, limit=10):
        """Get recent malicious connections."""
        return self.malicious_connections[-limit:]

    def get_statistics(self):
        """Get monitoring statistics."""
        return {
            'enabled': self.enabled,
            'total_connections': self.stats['total_connections'],
            'blocked_connections': self.stats['blocked_connections'],
            'unique_ips_seen': len(self.stats['unique_ips']),
            'blacklist_size': len(self.ip_blacklist),
            'whitelist_size': len(self.ip_whitelist),
            'last_feed_update': self.stats['last_update'].isoformat() if self.stats['last_update'] else None,
            'malicious_connections_count': len(self.malicious_connections)
        }

    def get_top_connections(self, limit=10):
        """Get most frequent connection destinations."""
        ip_counts = {}
        for ip in self.stats['unique_ips']:
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Sort by count
        sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_ips[:limit]

    def check_ip_reputation(self, ip):
        """Check IP reputation (cached)."""
        # Check cache first
        if ip in self.threat_cache:
            cache_entry = self.threat_cache[ip]
            age = (datetime.now() - cache_entry['timestamp']).total_seconds()

            if age < self.cache_duration:
                return cache_entry['data']

        # Check blacklist
        if ip in self.ip_blacklist:
            result = {
                'malicious': True,
                'source': 'Local SRX Feed',
                'confidence': 100
            }
        else:
            result = {
                'malicious': False,
                'source': 'Local Check',
                'confidence': 0
            }

        # Cache result
        self.threat_cache[ip] = {
            'timestamp': datetime.now(),
            'data': result
        }

        return result

    def block_ip(self, ip):
        """
        Block IP address (placeholder - requires firewall integration).

        Note: Actual implementation would use iptables/firewalld/Windows Firewall
        """
        self.log_action("BLOCK_REQUESTED", f"IP block requested: {ip}")

        # Add to blacklist
        self.ip_blacklist.add(ip)

        # TODO: Implement actual firewall blocking
        # Linux: subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
        # Windows: subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', ...])

        return True

    def get_status(self):
        """Get agent status."""
        status = super().get_status()
        status.update(self.get_statistics())
        return status
