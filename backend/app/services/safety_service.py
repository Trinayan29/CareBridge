from typing import Any


EMERGENCY_KEYWORDS = [
    "chest pain",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "severe bleeding",
    "unconscious",
    "loss of consciousness",
    "seizure",
    "stroke",
]


def check_safety(
    title: str,
    description: str,
) -> dict[str, Any]:
    text = f"{title} {description}".lower()

    matched_keywords = [
        keyword
        for keyword in EMERGENCY_KEYWORDS
        if keyword in text
    ]

    if matched_keywords:
        return {
            "is_emergency": True,
            "matched_keywords": matched_keywords,
            "message": (
                "The information provided contains a potential "
                "emergency warning sign. Seek immediate medical "
                "attention or contact your local emergency service."
            ),
        }

    return {
        "is_emergency": False,
        "matched_keywords": [],
        "message": "No predefined emergency keyword was detected.",
    }