import uuid


def new_request_id() -> str:
    return str(uuid.uuid4())


def clamp_text(s: str, max_chars: int) -> str:
    s = s.strip()
    if len(s) > max_chars:
        return s[:max_chars] + "\n\n[TRUNCATED]"
    return s