"""
Response Parser for IVE-LLM
============================
Multi-stage parser that extracts donation amounts, Likert ratings, allocation
splits, and meta-knowledge responses from potentially messy LLM output.

Pipeline:  exact match → case-insensitive regex → fuzzy extraction → failure
"""

import re
from dataclasses import dataclass, field
from typing import Optional

# ── Word-to-number mapping ───────────────────────────────────────────────────
_WORD_TO_NUM = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "no": 0, "none": 0,
}

_RATING_WORDS = {
    "not at all": 1, "slightly": 2, "moderately": 3, "very": 4, "extremely": 5,
    **{str(i): i for i in range(1, 6)},
}

_RATING_WORDS_7 = {
    "not at all": 1, "slightly": 2, "somewhat": 3, "moderately": 4,
    "quite": 5, "very": 6, "very much": 7, "extremely": 7,
    **{str(i): i for i in range(1, 8)},
}


@dataclass
class ParsedResponse:
    donation_amount: Optional[int] = None        # 0-5, None if unparseable
    rating_upsetting: Optional[int] = None       # 1-5
    rating_sympathetic: Optional[int] = None
    rating_moral_responsibility: Optional[int] = None
    rating_touched: Optional[int] = None
    rating_appropriate: Optional[int] = None
    feelings_composite: Optional[float] = None   # mean of 5 ratings
    reasoning_text: str = ""
    # Meta-knowledge (Experiment 2 extension)
    meta_awareness: Optional[bool] = None
    meta_influence_text: str = ""
    # Allocation (Experiment 4 extension)
    rokia_donation: Optional[float] = None
    general_fund: Optional[float] = None
    kept: Optional[float] = None
    # ── Extended emotion ratings (Kogut & Ritov / Batson scales, 1-7) ────
    # Distress subscale
    rating_worried: Optional[int] = None
    rating_upset: Optional[int] = None
    rating_sad: Optional[int] = None
    rating_disturbed: Optional[int] = None
    rating_troubled: Optional[int] = None
    distress_composite: Optional[float] = None
    # Empathic concern subscale
    rating_sympathy: Optional[int] = None
    rating_compassion: Optional[int] = None
    rating_tender: Optional[int] = None
    rating_moved: Optional[int] = None
    rating_softhearted: Optional[int] = None
    empathy_composite: Optional[float] = None
    # General (1-7)
    rating_moral_responsibility_7: Optional[int] = None
    rating_appropriate_7: Optional[int] = None
    # Parsing metadata
    parse_success: bool = False
    parse_method: str = "failed"
    raw_response: str = ""
    unparsed_fields: list = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def parse_response(raw_text: str, experiment_type: str = "standard") -> ParsedResponse:
    """
    Parse an LLM response into structured fields.

    Parameters
    ----------
    raw_text : str
        Full LLM output.
    experiment_type : str
        "standard" | "allocation" | "meta" | "allocation_meta"

    Returns
    -------
    ParsedResponse
    """
    result = ParsedResponse(raw_response=raw_text)

    # 1. Try exact format
    method, success = _try_exact(raw_text, result)
    if success:
        result.parse_method = "exact"
        result.parse_success = True
    else:
        # 2. Try regex
        method, success = _try_regex(raw_text, result)
        if success:
            result.parse_method = "regex"
            result.parse_success = True
        else:
            # 3. Fuzzy fallback
            method, success = _try_fuzzy(raw_text, result)
            if success:
                result.parse_method = "fuzzy"
                result.parse_success = True
            else:
                result.parse_method = "failed"
                result.parse_success = False

    # Coerce / validate ranges
    result.donation_amount = _clamp(result.donation_amount, 0, 5)
    for attr in ["rating_upsetting", "rating_sympathetic",
                 "rating_moral_responsibility", "rating_touched",
                 "rating_appropriate"]:
        setattr(result, attr, _clamp(getattr(result, attr), 1, 5))

    # Compute feelings composite
    ratings = [
        result.rating_upsetting, result.rating_sympathetic,
        result.rating_moral_responsibility, result.rating_touched,
        result.rating_appropriate,
    ]
    valid = [r for r in ratings if r is not None]
    if valid:
        result.feelings_composite = round(sum(valid) / len(valid), 3)

    # Extract reasoning if not yet set
    if not result.reasoning_text:
        result.reasoning_text = extract_reasoning(raw_text)

    # Parse allocation fields
    if experiment_type in ("allocation", "allocation_meta"):
        _parse_allocation(raw_text, result)

    # Parse meta-knowledge
    if experiment_type in ("meta", "allocation_meta"):
        _parse_meta(raw_text, result)

    # Determine what's missing
    if result.donation_amount is None:
        result.unparsed_fields.append("donation_amount")
    for attr in ["rating_upsetting", "rating_sympathetic",
                 "rating_moral_responsibility", "rating_touched",
                 "rating_appropriate"]:
        if getattr(result, attr) is None:
            result.unparsed_fields.append(attr)

    # Mark success only if donation_amount was parsed
    if result.donation_amount is None:
        result.parse_success = False

    return result


def extract_reasoning(raw_text: str) -> str:
    """Extract free-text reasoning from the response."""
    # Look for REASONING: tag
    m = re.search(r"REASONING:\s*(.+)", raw_text, re.IGNORECASE | re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Trim at the next tag if any
        text = re.split(r"\n[A-Z_]+:", text)[0].strip()
        return text
    # Fallback: last paragraph
    paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
    if paragraphs:
        return paragraphs[-1]
    return ""


# ═══════════════════════════════════════════════════════════════════════════════
#  STAGE 1: EXACT FORMAT MATCH
# ═══════════════════════════════════════════════════════════════════════════════

def _try_exact(text: str, result: ParsedResponse) -> tuple:
    fields_found = 0

    def _match(pattern, txt):
        return re.search(pattern, txt, re.MULTILINE)

    m = _match(r"^DONATION:\s*\$(\d)", text)
    if m:
        result.donation_amount = int(m.group(1))
        fields_found += 1

    for tag, attr in [
        ("UPSETTING", "rating_upsetting"),
        ("SYMPATHETIC", "rating_sympathetic"),
        ("MORAL_RESPONSIBILITY", "rating_moral_responsibility"),
        ("TOUCHED", "rating_touched"),
        ("APPROPRIATE", "rating_appropriate"),
    ]:
        m = _match(rf"^{tag}:\s*(\d)", text)
        if m:
            setattr(result, attr, int(m.group(1)))
            fields_found += 1

    # All 6 core fields matched?
    return "exact", fields_found == 6


# ═══════════════════════════════════════════════════════════════════════════════
#  STAGE 2: CASE-INSENSITIVE REGEX
# ═══════════════════════════════════════════════════════════════════════════════

def _try_regex(text: str, result: ParsedResponse) -> tuple:
    fields_found = 0
    ci = re.IGNORECASE | re.MULTILINE

    # Donation
    if result.donation_amount is None:
        patterns = [
            r"donation[:\s]*\$(\d)",
            r"donate[:\s]*\$(\d)",
            r"(?:would|will|should)\s+donate\s+\$(\d)",
            r"\$(\d)(?:\.00)?\b",
        ]
        for p in patterns:
            m = re.search(p, text, ci)
            if m:
                result.donation_amount = int(m.group(1))
                fields_found += 1
                break

    # Ratings
    rating_patterns = {
        "rating_upsetting": [r"upsetting[:\s]*(\d)", r"upset[:\s]*(\d)"],
        "rating_sympathetic": [r"sympathetic[:\s]*(\d)", r"sympathy[:\s]*(\d)"],
        "rating_moral_responsibility": [r"moral[_ ]?responsibility[:\s]*(\d)", r"moral[:\s]*(\d)"],
        "rating_touched": [r"touched[:\s]*(\d)"],
        "rating_appropriate": [r"appropriate[:\s]*(\d)"],
    }
    for attr, pats in rating_patterns.items():
        if getattr(result, attr) is None:
            for p in pats:
                m = re.search(p, text, ci)
                if m:
                    setattr(result, attr, int(m.group(1)))
                    fields_found += 1
                    break

    return "regex", fields_found >= 3  # at least donation + 2 ratings


# ═══════════════════════════════════════════════════════════════════════════════
#  STAGE 3: FUZZY FALLBACK
# ═══════════════════════════════════════════════════════════════════════════════

def _try_fuzzy(text: str, result: ParsedResponse) -> tuple:
    lower = text.lower()

    # Donation: look for dollar amounts or number words
    if result.donation_amount is None:
        # Check for word numbers near "donate"
        for word, num in _WORD_TO_NUM.items():
            if word in lower and ("donat" in lower or "give" in lower):
                result.donation_amount = num
                break
        # Last resort: first standalone dollar amount 0-5
        if result.donation_amount is None:
            m = re.search(r"\$([0-5])(?:\.00)?", text)
            if m:
                result.donation_amount = int(m.group(1))

    # Ratings: look for numbers near keywords
    kw_map = {
        "rating_upsetting": ["upsetting", "upset", "distressing"],
        "rating_sympathetic": ["sympathetic", "sympathy", "empathetic"],
        "rating_moral_responsibility": ["moral", "responsibility", "obligation"],
        "rating_touched": ["touched", "moved", "affected"],
        "rating_appropriate": ["appropriate", "fitting", "suitable"],
    }
    for attr, keywords in kw_map.items():
        if getattr(result, attr) is not None:
            continue
        for kw in keywords:
            idx = lower.find(kw)
            if idx != -1:
                window = text[max(0, idx - 20):idx + len(kw) + 30]
                m = re.search(r"[:\s]([1-5])\b", window)
                if m:
                    setattr(result, attr, int(m.group(1)))
                    break
                # Try rating words
                for rw, rv in _RATING_WORDS.items():
                    if rw in window.lower():
                        setattr(result, attr, rv)
                        break

    # Numbered list fallback: "1. 4" "2. 5" etc.
    numbered_items = re.findall(r"(\d)\.\s*(\d)\b", text)
    rating_attrs = [
        "rating_upsetting", "rating_sympathetic",
        "rating_moral_responsibility", "rating_touched", "rating_appropriate"
    ]
    for item_num_str, value_str in numbered_items:
        item_num = int(item_num_str)
        value = int(value_str)
        if 1 <= item_num <= 5 and 1 <= value <= 5:
            idx = item_num - 1
            if getattr(result, rating_attrs[idx]) is None:
                setattr(result, rating_attrs[idx], value)

    return "fuzzy", result.donation_amount is not None


# ═══════════════════════════════════════════════════════════════════════════════
#  ALLOCATION PARSER (Experiment 4)
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_allocation(text: str, result: ParsedResponse) -> None:
    ci = re.IGNORECASE

    m = re.search(r"ROKIA[_ ]?DONATION[:\s]*\$?([\d.]+)", text, ci)
    if m:
        try:
            result.rokia_donation = float(m.group(1))
        except ValueError:
            pass

    m = re.search(r"GENERAL[_ ]?FUND[:\s]*\$?([\d.]+)", text, ci)
    if m:
        try:
            result.general_fund = float(m.group(1))
        except ValueError:
            pass

    m = re.search(r"KEPT[:\s]*\$?([\d.]+)", text, ci)
    if m:
        try:
            result.kept = float(m.group(1))
        except ValueError:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
#  META-KNOWLEDGE PARSER (Experiment 2)
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_meta(text: str, result: ParsedResponse) -> None:
    ci = re.IGNORECASE

    m = re.search(r"META[_ ]?AWARENESS[:\s]*(yes|no)", text, ci)
    if m:
        result.meta_awareness = m.group(1).lower() == "yes"
    else:
        lower = text.lower()
        if "identifiable victim effect" in lower:
            if any(w in lower for w in ["yes", "aware", "familiar", "know of", "i am aware"]):
                result.meta_awareness = True
            elif any(w in lower for w in ["no", "not aware", "unfamiliar"]):
                result.meta_awareness = False

    m = re.search(r"META[_ ]?INFLUENCE[:\s]*(.+?)(?:\n[A-Z_]+:|$)", text, ci | re.DOTALL)
    if m:
        result.meta_influence_text = m.group(1).strip()


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _clamp(value: Optional[int], lo: int, hi: int) -> Optional[int]:
    if value is None:
        return None
    return max(lo, min(hi, value))


# ═══════════════════════════════════════════════════════════════════════════════
#  EXTENDED PARSER (Experiments 8-10)
# ═══════════════════════════════════════════════════════════════════════════════

# Maps tag names → (ParsedResponse attribute, scale_max)
_EXTENDED_TAGS = {
    "WORRIED": ("rating_worried", 7),
    "UPSET": ("rating_upset", 7),
    "SAD": ("rating_sad", 7),
    "DISTURBED": ("rating_disturbed", 7),
    "TROUBLED": ("rating_troubled", 7),
    "SYMPATHY": ("rating_sympathy", 7),
    "COMPASSION": ("rating_compassion", 7),
    "TENDER": ("rating_tender", 7),
    "MOVED": ("rating_moved", 7),
    "SOFTHEARTED": ("rating_softhearted", 7),
    "MORAL_RESPONSIBILITY": ("rating_moral_responsibility_7", 7),
    "APPROPRIATE": ("rating_appropriate_7", 7),
}


def parse_response_extended(raw_text: str) -> ParsedResponse:
    """
    Parse the extended 12-item response format (1-7 scales).

    Auto-detects which format was used and parses all available fields.
    Computes distress_composite and empathy_composite when all constituent
    items are present.
    """
    result = ParsedResponse(raw_response=raw_text)
    ci = re.IGNORECASE | re.MULTILINE

    # ── Donation ─────────────────────────────────────────────────────────
    m = re.search(r"DONATION[:\s]*\$?([0-5])", raw_text, ci)
    if m:
        result.donation_amount = int(m.group(1))
    else:
        # Fallback: any dollar amount 0-5
        m = re.search(r"\$([0-5])(?:\.00)?\b", raw_text)
        if m:
            result.donation_amount = int(m.group(1))

    # ── Extended emotion ratings ─────────────────────────────────────────
    for tag, (attr, scale_max) in _EXTENDED_TAGS.items():
        # Exact tag match
        m = re.search(rf"^{tag}[:\s]*(\d)\b", raw_text, ci | re.MULTILINE)
        if m:
            val = int(m.group(1))
            setattr(result, attr, max(1, min(scale_max, val)))
            continue
        # Looser match
        m = re.search(rf"{tag}[:\s]*(\d)\b", raw_text, ci)
        if m:
            val = int(m.group(1))
            setattr(result, attr, max(1, min(scale_max, val)))
            continue
        # Keyword window fallback
        kw = tag.lower().replace("_", " ")
        idx = raw_text.lower().find(kw)
        if idx != -1:
            window = raw_text[idx:idx + len(kw) + 40]
            m = re.search(r"[:\s]([1-7])\b", window)
            if m:
                setattr(result, attr, int(m.group(1)))

    # ── Numbered list fallback (1. X  2. Y  ... 12. Z) ──────────────────
    numbered = re.findall(r"(\d{1,2})\.\s*(\d)\b", raw_text)
    ext_attrs = [
        "rating_worried", "rating_upset", "rating_sad", "rating_disturbed",
        "rating_troubled", "rating_sympathy", "rating_compassion",
        "rating_tender", "rating_moved", "rating_softhearted",
        "rating_moral_responsibility_7", "rating_appropriate_7",
    ]
    for item_str, val_str in numbered:
        item_num = int(item_str)
        val = int(val_str)
        if 1 <= item_num <= 12 and 1 <= val <= 7:
            idx_attr = item_num - 1
            if getattr(result, ext_attrs[idx_attr]) is None:
                setattr(result, ext_attrs[idx_attr], val)

    # ── Composites ───────────────────────────────────────────────────────
    distress_items = [
        result.rating_worried, result.rating_upset, result.rating_sad,
        result.rating_disturbed, result.rating_troubled,
    ]
    valid_d = [r for r in distress_items if r is not None]
    if len(valid_d) >= 3:  # at least 3 of 5 for a partial composite
        result.distress_composite = round(sum(valid_d) / len(valid_d), 3)

    empathy_items = [
        result.rating_sympathy, result.rating_compassion, result.rating_tender,
        result.rating_moved, result.rating_softhearted,
    ]
    valid_e = [r for r in empathy_items if r is not None]
    if len(valid_e) >= 3:
        result.empathy_composite = round(sum(valid_e) / len(valid_e), 3)

    # ── Reasoning ────────────────────────────────────────────────────────
    result.reasoning_text = extract_reasoning(raw_text)

    # ── Parse success ────────────────────────────────────────────────────
    parsed_count = sum(
        1 for attr in ext_attrs if getattr(result, attr) is not None
    )
    if result.donation_amount is not None and parsed_count >= 6:
        result.parse_success = True
        result.parse_method = "extended_exact" if parsed_count >= 10 else "extended_partial"
    elif result.donation_amount is not None:
        result.parse_success = True
        result.parse_method = "extended_donation_only"
    else:
        result.parse_method = "failed"

    # Track unparsed fields
    if result.donation_amount is None:
        result.unparsed_fields.append("donation_amount")
    for attr in ext_attrs:
        if getattr(result, attr) is None:
            result.unparsed_fields.append(attr)

    return result
