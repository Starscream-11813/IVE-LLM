"""
Linguistic Analysis for IVE-LLM
================================
Extracts linguistic features from free-text LLM reasoning:
  - Sympathy / utilitarian / hedging marker counts & densities
  - Personal pronoun & statistical / individual language densities
  - Sentiment polarity & subjectivity (TextBlob)
  - Reasoning type classification
"""

from dataclasses import dataclass, field
from typing import List
import re

from textblob import TextBlob

# ═══════════════════════════════════════════════════════════════════════════════
#  KEYWORD DICTIONARIES
# ═══════════════════════════════════════════════════════════════════════════════

SYMPATHY_MARKERS = {
    "sympathy", "sympathetic", "empathy", "empathetic", "compassion",
    "pity", "sorry", "heart", "heartbreaking", "heartfelt", "touching",
    "moved", "care", "caring", "concern", "worried", "distressed", "ache",
    "suffer", "suffering", "pain", "painful", "tragic", "tragedy",
    "devastating", "desperate", "helpless", "vulnerable", "innocent",
    "poor", "needy",
}

UTILITARIAN_MARKERS = {
    "efficient", "efficiency", "effective", "effectiveness", "maximize",
    "optimal", "rational", "cost-benefit", "impact", "scale", "marginal",
    "utility", "aggregate", "total", "expected value", "per dollar",
    "cost-effective", "allocation", "resources", "systematic", "strategic",
    "prioritize", "triage", "evidence-based", "measurable",
}

HEDGING_MARKERS = {
    "perhaps", "maybe", "might", "could", "possibly", "arguably",
    "it depends", "hard to say", "difficult to", "not sure", "uncertain",
    "on one hand", "on the other hand", "however", "although", "but",
}

PERSONAL_PRONOUNS = {
    "i", "me", "my", "mine", "myself",
    "she", "he", "her", "him", "his",
    "they", "them", "their",
}

STATISTICAL_LANGUAGE = {
    "million", "thousand", "percent", "percentage", "data",
    "statistics", "number", "numbers", "population", "rate", "ratio",
    "proportion", "average", "total", "overall", "aggregate", "mass",
}

INDIVIDUAL_LANGUAGE = {
    "child", "girl", "boy", "name", "she", "he", "her",
    "him", "face", "life", "story", "family", "person", "individual",
    "someone", "one person",
}

# ═══════════════════════════════════════════════════════════════════════════════
#  DATACLASS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class LinguisticFeatures:
    # Counts
    word_count: int = 0
    sentence_count: int = 0
    sympathy_marker_count: int = 0
    utilitarian_marker_count: int = 0
    hedging_marker_count: int = 0
    personal_pronoun_count: int = 0
    statistical_language_count: int = 0
    individual_language_count: int = 0
    # Densities (per 100 words)
    sympathy_density: float = 0.0
    utilitarian_density: float = 0.0
    hedging_density: float = 0.0
    personal_pronoun_density: float = 0.0
    statistical_language_density: float = 0.0
    individual_language_density: float = 0.0
    # Sentiment
    sentiment_polarity: float = 0.0       # -1 to 1
    sentiment_subjectivity: float = 0.0   # 0 to 1
    # Derived
    emotion_vs_logic_ratio: float = 0.0
    reasoning_type: str = "neutral"
    # Raw lists
    sympathy_words_found: List[str] = field(default_factory=list)
    utilitarian_words_found: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_text(text: str) -> LinguisticFeatures:
    """Run full linguistic analysis pipeline on a text string."""
    if not text or not text.strip():
        return LinguisticFeatures()

    feat = LinguisticFeatures()
    lower = text.lower()
    words = re.findall(r"\b[a-z']+\b", lower)
    feat.word_count = len(words)
    feat.sentence_count = max(1, len(re.split(r"[.!?]+", text.strip())))

    if feat.word_count == 0:
        return feat

    # ── Marker counting ──────────────────────────────────────────────────
    def _count_markers(marker_set):
        found = []
        for marker in marker_set:
            # Multi-word markers: check in full text
            if " " in marker:
                cnt = lower.count(marker)
                if cnt > 0:
                    found.extend([marker] * cnt)
            else:
                cnt = words.count(marker)
                if cnt > 0:
                    found.extend([marker] * cnt)
        return found

    sym_found = _count_markers(SYMPATHY_MARKERS)
    feat.sympathy_marker_count = len(sym_found)
    feat.sympathy_words_found = list(set(sym_found))

    util_found = _count_markers(UTILITARIAN_MARKERS)
    feat.utilitarian_marker_count = len(util_found)
    feat.utilitarian_words_found = list(set(util_found))

    feat.hedging_marker_count = len(_count_markers(HEDGING_MARKERS))
    feat.personal_pronoun_count = sum(1 for w in words if w in PERSONAL_PRONOUNS)
    feat.statistical_language_count = len(_count_markers(STATISTICAL_LANGUAGE))
    feat.individual_language_count = len(_count_markers(INDIVIDUAL_LANGUAGE))

    # ── Densities (per 100 words) ────────────────────────────────────────
    n = feat.word_count
    feat.sympathy_density = round(feat.sympathy_marker_count / n * 100, 3)
    feat.utilitarian_density = round(feat.utilitarian_marker_count / n * 100, 3)
    feat.hedging_density = round(feat.hedging_marker_count / n * 100, 3)
    feat.personal_pronoun_density = round(feat.personal_pronoun_count / n * 100, 3)
    feat.statistical_language_density = round(feat.statistical_language_count / n * 100, 3)
    feat.individual_language_density = round(feat.individual_language_count / n * 100, 3)

    # ── Sentiment ────────────────────────────────────────────────────────
    blob = TextBlob(text)
    feat.sentiment_polarity = round(blob.sentiment.polarity, 4)
    feat.sentiment_subjectivity = round(blob.sentiment.subjectivity, 4)

    # ── Derived ──────────────────────────────────────────────────────────
    feat.emotion_vs_logic_ratio = round(
        feat.sympathy_density / (feat.utilitarian_density + 0.001), 3
    )
    feat.reasoning_type = classify_reasoning_type(feat)

    return feat


def classify_reasoning_type(feat: LinguisticFeatures) -> str:
    """
    Classify reasoning as:
      - "emotional"   : sympathy_density > utilitarian_density * 2
      - "utilitarian"  : utilitarian_density > sympathy_density * 2
      - "mixed"        : both present in similar amounts
      - "neutral"      : neither significantly present
    """
    s = feat.sympathy_density
    u = feat.utilitarian_density
    threshold = 0.5  # minimum density to register

    if s < threshold and u < threshold:
        return "neutral"
    if s > u * 2:
        return "emotional"
    if u > s * 2:
        return "utilitarian"
    return "mixed"
