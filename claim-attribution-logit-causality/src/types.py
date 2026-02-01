"""
Core type definitions for the Claim Attribution via Logit Causality system.

This file defines the *shared vocabulary* used across the project:
- what a Claim is
- what a Span is
- how spans are classified
- how roles are assigned post-hoc

No logic should live here.
Only types, enums, and data containers.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List


class ClaimType(str, Enum):
    """
    Represents the type of claim we are trying to attribute.

    This project is intentionally conservative.
    For v1, we only support *factual claims*.

    Future claim types (NOT implemented yet) could include:
    - numerical
    - causal
    - normative
    """
    FACTUAL = "factual"
    
class SpanClass(str, Enum):
    """
    Structural classification of prompt spans.

    SpanClass answers the question:
    "What *kind* of text is this span?"

    IMPORTANT:
    - SpanClass does NOT imply causality
    - It is only used to organize testing and caching
    """

    INTERROGATIVE = "interrogative"      # Questions like: "What is X?"
    CODE_BLOCK = "code_block"            # Fenced or multiline code
    ASSIGNMENT = "assignment"            # Code assignments like: y = 0
    INSTRUCTION = "instruction"          # Style/format instructions
    CONTEXT = "context"                  # Background or framing text
    UNKNOWN = "unknown"                  # Fallback: always tested, never skipped
    
class SpanRole(str, Enum):
    """
    Post-hoc causal role of a span.

    SpanRole answers the question:
    "What effect does this span have on the claim?"

    IMPORTANT:
    - Roles are NEVER assigned in advance
    - Roles are inferred ONLY after counterfactual testing
    """

    PRIMARY_QUERY = "primary_query"
    # Removing this span collapses the claim completely

    INSTRUCTIONAL_MODIFIER = "instructional_modifier"
    # Removing this span changes style/format but not the fact

    CONTEXTUAL_BACKGROUND = "contextual_background"
    # Removing this span has minimal or no effect

    UNASSIGNED = "unassigned"
    # Initial state before any causal testing
    
@dataclass
class Span:
    """
    Represents a contiguous portion of the prompt.

    A Span is the *unit of counterfactual testing*.

    Fields:
    - text: the literal span text
    - span_class: structural category (pre-counterfactual)
    - role: causal role (post-counterfactual, initially UNASSIGNED)
    """

    text: str
    span_class: SpanClass
    role: SpanRole = SpanRole.UNASSIGNED

@dataclass
class Claim:
    """
    Represents the claim we are trying to causally explain.

    A Claim is ALWAYS extracted from the model's output,
    never from the prompt.

    Fields:
    - text: human-readable claim string (e.g. "Paris")
    - claim_type: currently only FACTUAL
    - token_ids: tokenized form used for probability computation
    """

    text: str
    claim_type: ClaimType
    token_ids: List[int]