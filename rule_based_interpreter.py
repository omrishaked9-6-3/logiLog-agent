import re
from datetime import datetime

def interpret_block(block_lines):
    """
    Interprets a block of log lines using simple rule-based logic.
    Detects lines with ERROR, WARN, EXCEPTION, etc.
    Returns a list of alert dicts.
    """
    alerts = []

    for line in block_lines:
        lower = line.lower()

        if any(keyword in lower for keyword in ["error", "exception", "fail", "warn", "critical", "refused"]):
            alert = {
                "timestamp": extract_timestamp(line),
                "level": extract_level(line),
                "message": line,
                "interpretation": interpret_message(line),
                "critical": "error" in lower or "exception" in lower or "fail" in lower
            }
            alerts.append(alert)

    return alerts


def extract_timestamp(line):
    """
    Extracts timestamp from beginning of log line if it exists.
    """
    match = re.match(r"^(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}[,\\.]?\\d*)", line)
    if match:
        return match.group(1)
    return datetime.now().isoformat()


def extract_level(line):
    """
    Extracts log level based on common keywords.
    """
    for level in ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "FATAL"]:
        if level.lower() in line.lower():
            return level.upper()
    return "UNKNOWN"


def interpret_message(line):
    """
    Provides a basic interpretation of the issue in the log line.
    """
    lower = line.lower()
    if "database" in lower and ("fail" in lower or "refused" in lower):
        return "Database connection issue"
    if "timeout" in lower:
        return "Operation timed out"
    if "unauthorized" in lower or "403" in lower:
        return "Access denied or unauthorized request"
    if "nullpointer" in lower or "null" in lower:
        return "Possible null reference bug"
    if "exception" in lower:
        return "Unhandled exception"
    if "error" in lower:
        return "General error"
    if "warn" in lower:
        return "Potential issue - warning"
    return "Suspicious or unexpected behavior"
