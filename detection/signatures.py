"""
Malware Signatures and Pattern Database
"""

# Known malware file hashes (SHA-256)
# In production, this would be a much larger database
MALWARE_HASHES = {
    # EICAR test file hash
    '275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f': 'EICAR-Test-File',
    '44d88612fea8a8f36de82e1278abb02f': 'EICAR-Test-File-MD5',  # MD5 version

    # Add more known malware hashes here
    # These would come from threat intelligence feeds
}

# Suspicious file patterns (regex patterns to search in file content)
MALWARE_PATTERNS = [
    # Windows executable patterns
    (b'MZ\x90\x00', 'PE_EXECUTABLE', 'Windows executable header'),
    (b'\x4d\x5a\x90\x00', 'PE_EXECUTABLE', 'Windows PE header'),

    # Script patterns
    (b'eval(', 'SUSPICIOUS_SCRIPT', 'Eval function (code execution)'),
    (b'exec(', 'SUSPICIOUS_SCRIPT', 'Exec function (code execution)'),
    (b'system(', 'SUSPICIOUS_SCRIPT', 'System call'),

    # Suspicious strings
    (b'trojan', 'MALWARE_KEYWORD', 'Trojan keyword'),
    (b'backdoor', 'MALWARE_KEYWORD', 'Backdoor keyword'),
    (b'keylog', 'MALWARE_KEYWORD', 'Keylogger keyword'),
    (b'ransomware', 'MALWARE_KEYWORD', 'Ransomware keyword'),
    (b'cryptolcker', 'MALWARE_KEYWORD', 'Cryptolocker variant'),

    # Network/C&C patterns
    (b'http://malware', 'MALICIOUS_URL', 'Malicious URL pattern'),
    (b'.onion', 'TOR_ADDRESS', 'Tor hidden service'),

    # Registry manipulation
    (b'HKEY_LOCAL_MACHINE', 'REGISTRY_ACCESS', 'Registry access'),
    (b'HKEY_CURRENT_USER', 'REGISTRY_ACCESS', 'Registry access'),

    # Encoding/obfuscation
    (b'base64', 'ENCODING', 'Base64 encoding present'),
    (b'chr(', 'OBFUSCATION', 'Character code obfuscation'),
]

# Suspicious keywords in filenames
FILENAME_KEYWORDS = [
    'crack', 'keygen', 'patch', 'activator', 'generator',
    'hack', 'cheat', 'exploit', 'payload', 'backdoor',
    'password', 'stealer', 'logger', 'rat', 'trojan',
    'virus', 'malware', 'ransomware', 'worm', 'rootkit',
    'bitcoin', 'wallet', 'miner', 'crypter', 'injector'
]

# High risk file extensions
HIGH_RISK_EXTENSIONS = {
    '.exe': 40,
    '.scr': 40,  # Screensaver
    '.vbs': 35,  # VBScript
    '.bat': 30,  # Batch file
    '.cmd': 30,  # Command script
    '.com': 40,  # DOS executable
    '.pif': 35,  # Program Information File
    '.application': 35,
    '.gadget': 35,
    '.msi': 30,  # Installer
    '.jar': 25,  # Java archive
    '.hta': 35,  # HTML Application
    '.cpl': 35,  # Control Panel
    '.ps1': 30,  # PowerShell
    '.sh': 25,   # Shell script
    '.app': 25,  # Mac application
    '.deb': 20,  # Debian package
    '.rpm': 20,  # RPM package
}

# Medium risk file extensions
MEDIUM_RISK_EXTENSIONS = {
    '.zip': 15,
    '.rar': 15,
    '.7z': 15,
    '.gz': 10,
    '.tar': 10,
    '.pdf': 10,
    '.doc': 15,
    '.docx': 15,
    '.xls': 15,
    '.xlsx': 15,
    '.ppt': 10,
    '.pptx': 10,
    '.js': 20,   # JavaScript
    '.wsf': 25,  # Windows Script File
    '.wsh': 25,  # Windows Script Host
}

def get_extension_risk(extension: str) -> tuple:
    """
    Get risk level for a file extension.

    Args:
        extension: File extension (including dot)

    Returns:
        Tuple of (risk_score, risk_level)
    """
    extension = extension.lower()

    if extension in HIGH_RISK_EXTENSIONS:
        return (HIGH_RISK_EXTENSIONS[extension], 'HIGH')
    elif extension in MEDIUM_RISK_EXTENSIONS:
        return (MEDIUM_RISK_EXTENSIONS[extension], 'MEDIUM')
    else:
        return (0, 'LOW')


def check_filename_suspicious(filename: str) -> tuple:
    """
    Check if filename contains suspicious keywords.

    Args:
        filename: Name of the file

    Returns:
        Tuple of (score, matched_keywords)
    """
    score = 0
    matched = []

    filename_lower = filename.lower()

    for keyword in FILENAME_KEYWORDS:
        if keyword in filename_lower:
            score += 20
            matched.append(keyword)

    return (min(score, 60), matched)  # Cap at 60
