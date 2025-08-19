from typing import Optional

def classify_body_type_dummy(image_bytes: bytes) -> str:
    """Dummy classifier to simulate CV output. Replace with real model integration later.
    Heuristic: return 'sedan' if file size mod 3 == 0, 'suv' if mod 3 ==1, else 'hatchback'.
    """
    if not image_bytes:
        return "unknown"
    m = len(image_bytes) % 3
    if m == 0:
        return "sedan"
    if m == 1:
        return "suv"
    return "hatchback"
