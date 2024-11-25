import re
from typing import Optional

def extract_channel_id(link: str) -> Optional[str]:
    """Extract channel ID from telegram link."""
    match = re.search(r"t\.me/([^/]+)", link)
    if match:
        return match.group(1)
    return None

def is_valid_bot_token(token: str) -> bool:
    """Validate bot token format."""
    return bool(re.match(r'^[\d\w\-_]{20,}:[\w\-]{35,}$', token))