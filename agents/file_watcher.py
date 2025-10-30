"""
File Watcher Agent
Monitors file system for new downloads and suspicious file activity.
"""

import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .base_agent import BaseSecurityAgent


class FileEventHandler(FileSystemEventHandler):
    """Handles file system events."""

    def __init__(self, agent):
        """Initialize with reference to parent agent."""
        self.agent = agent
        super().__init__()

    def on_created(self, event):
        """Called when a file is created."""
        if not event.is_directory:
            self.agent.handle_new_file(event.src_path)

    def on_modified(self, event):
        """Called when a file is modified."""
        if not event.is_directory:
            # Only track significant modifications
            pass


class FileWatcherAgent(BaseSecurityAgent):
    """Agent that monitors file system for new and suspicious files."""

    def __init__(self, name="FileWatcher", watch_paths=None):
        """
        Initialize file watcher agent.

        Args:
            name: Agent name
            watch_paths: List of paths to monitor
        """
        super().__init__(name, "watcher")

        if watch_paths is None:
            # Default monitoring locations
            home = os.path.expanduser("~")
            watch_paths = [
                os.path.join(home, "Downloads"),
                os.path.join(home, "Desktop"),
                os.path.join(home, "Documents"),
            ]

        self.watch_paths = [p for p in watch_paths if os.path.exists(p)]
        self.observers = []
        self.files_detected = []

    def run(self):
        """Main monitoring loop."""
        self.log_action("INIT", f"Starting file monitoring on {len(self.watch_paths)} locations")

        # Set up observers for each watch path
        for path in self.watch_paths:
            event_handler = FileEventHandler(self)
            observer = Observer()
            observer.schedule(event_handler, path, recursive=False)
            observer.start()
            self.observers.append(observer)
            self.log_action("WATCHING", f"Monitoring: {path}")

        # Keep running while active
        try:
            while self.active:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop all observers and the agent."""
        for observer in self.observers:
            observer.stop()
            observer.join()
        super().stop()

    def handle_new_file(self, file_path: str):
        """
        Handle detection of a new file.

        Args:
            file_path: Path to the new file
        """
        # Skip temporary files and hidden files
        filename = os.path.basename(file_path)
        if filename.startswith('.') or filename.endswith('.tmp'):
            return

        # Wait a moment for file to finish writing
        time.sleep(0.5)

        # Check if file still exists and is readable
        if not os.path.exists(file_path):
            return

        # Gather file metadata
        try:
            file_info = self.gather_file_info(file_path)
            self.files_detected.append(file_info)

            # Calculate initial priority
            priority = self.calculate_priority(file_info)

            # Report to coordinator
            self.report_to_coordinator({
                'event_type': 'FILE_DETECTED',
                'file_info': file_info,
                'priority': priority,
                'timestamp': datetime.now()
            })

            self.log_action(
                "FILE_DETECTED",
                f"New file: {file_info['name']} (Size: {file_info['size']} bytes, Priority: {priority})"
            )

        except Exception as e:
            self.log_action("ERROR", f"Error processing {file_path}: {str(e)}")

    def gather_file_info(self, file_path: str) -> dict:
        """
        Gather metadata about a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        stat = os.stat(file_path)

        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1].lower(),
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'directory': os.path.dirname(file_path)
        }

    def calculate_priority(self, file_info: dict) -> int:
        """
        Calculate initial priority score for a file.

        Args:
            file_info: File metadata

        Returns:
            Priority score (0-100)
        """
        priority = 0

        # Check extension risk
        high_risk_extensions = [
            '.exe', '.scr', '.vbs', '.bat', '.cmd', '.com',
            '.pif', '.application', '.gadget', '.msi', '.jar',
            '.hta', '.cpl', '.ps1', '.sh'
        ]

        medium_risk_extensions = [
            '.zip', '.rar', '.7z', '.gz', '.tar',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx'
        ]

        if file_info['extension'] in high_risk_extensions:
            priority += 40
        elif file_info['extension'] in medium_risk_extensions:
            priority += 20

        # Check for double extensions (e.g., .pdf.exe)
        if file_info['name'].count('.') > 1:
            priority += 30

        # Check file size anomalies
        size = file_info['size']
        if size < 1024:  # Very small files are suspicious
            priority += 15
        elif size > 100_000_000:  # Very large files (>100MB)
            priority += 10

        # Check for suspicious keywords in filename
        suspicious_keywords = [
            'crack', 'keygen', 'patch', 'hack', 'cheat',
            'password', 'bitcoin', 'wallet', 'invoice',
            'virus', 'trojan', 'malware'
        ]

        name_lower = file_info['name'].lower()
        for keyword in suspicious_keywords:
            if keyword in name_lower:
                priority += 20
                break

        # Check download time (downloads at odd hours more suspicious)
        hour = datetime.now().hour
        if hour < 6 or hour > 23:  # Late night/early morning
            priority += 10

        return min(priority, 100)  # Cap at 100

    def get_status(self) -> dict:
        """Get agent status with monitoring details."""
        status = super().get_status()
        status.update({
            'watching_paths': self.watch_paths,
            'files_detected': len(self.files_detected),
            'recent_detections': self.files_detected[-5:] if self.files_detected else []
        })
        return status
