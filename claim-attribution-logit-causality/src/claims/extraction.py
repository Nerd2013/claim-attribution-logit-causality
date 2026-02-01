"""
Claim extraction logic.

This module identifies a single candidate factual claim
from the model's output text.

IMPORTANT:
- This is NOT semantic understanding.
- This is conservative pattern selection.
- If no clear claim is found, return None.
"""

from typing import Optional
from src.types import Claim, ClaimType


def _normalize_text(text: str) -> str:
    """
    Normalize model output text for claim extraction.

    - Strip whitespace
    - Remove surrounding quotes
    """
    return text.strip().strip('"').strip("'")

def extract_claim_from_answer(answer_text: str) -> Optional[Claim]:
    """
    Attempt to extract a single factual claim from the model's answer.

    Returns:
        Claim if a clear candidate is found
        None if extraction is ambiguous or unsafe

    This function MUST be conservative.
    """

    normalized = _normalize_text(answer_text)

    # 1️⃣ Empty or trivial output → no claim
    if not normalized:
        return None

    # 2️⃣ Single-token / short answer heuristic
    # Example: "Paris"
    if len(normalized.split()) <= 3:
        return Claim(
            text=normalized,
            claim_type=ClaimType.FACTUAL,
            token_ids=[]  # filled later after tokenization
        )

    # 3️⃣ Simple declarative sentence heuristic
    # Example: "The capital of France is Paris."
    if normalized.endswith("."):
        return Claim(
            text=normalized,
            claim_type=ClaimType.FACTUAL,
            token_ids=[]
        )

    # 4️⃣ Anything else is ambiguous → refuse
    return None