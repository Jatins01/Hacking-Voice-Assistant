import re

def check_url_phishing(url):
    suspicious_patterns = [
        r'@',
        r'-',
        r'https?:\/\/.*\.zip$',
        r'(login|verify|update)',
    ]
    for pattern in suspicious_patterns:
        if re.search(pattern, url.lower()):
            return "⚠️ Warning: This URL looks suspicious!"
    return "✅ URL seems safe."
