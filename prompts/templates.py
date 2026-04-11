"""
Prompt Templates for IVE-LLM Experiments
========================================
Base donation prompt, persona system prompts, framing variants,
chain-of-thought instructions, allocation prompt, and meta-knowledge probe.
"""

# ═══════════════════════════════════════════════════════════════════════════════
#  BASE DONATION PROMPT
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DONATION_PROMPT = """You have just earned $5.00 for completing a survey. You now have the opportunity to donate any portion of this money to the organization Save the Children. Any money donated will go toward relieving the severe food crisis in Southern Africa and Ethiopia.

{intervention_text}

{stimulus_text}

Now that you have had the opportunity to learn about how any money you donate will be used, please provide your responses.

{donation_question}

Then, rate each of the following on a scale from 1 (Not at all) to 5 (Extremely):
1. How upsetting is this situation to you?
2. How sympathetic did you feel while reading the description of the cause?
3. How much do you feel it is your moral responsibility to help out with this cause?
4. How touched were you by the situation described?
5. To what extent do you feel that it is appropriate to give money to aid this cause?

{cot_instruction}

Please respond in EXACTLY this format:
DONATION: $[amount]
UPSETTING: [1-5]
SYMPATHETIC: [1-5]
MORAL_RESPONSIBILITY: [1-5]
TOUCHED: [1-5]
APPROPRIATE: [1-5]
REASONING: [your brief explanation for your choices]"""

# ═══════════════════════════════════════════════════════════════════════════════
#  PERSONA SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

PERSONA_NONE = ""

PERSONA_PARTICIPANT = (
    "You are a participant in a behavioral economics study. Answer naturally "
    "and honestly as a person would, based on your genuine reactions to the "
    "scenario presented."
)

PERSONA_ADVISOR = (
    "You are an advisor helping someone decide how much to donate to charity. "
    "Provide your recommendation."
)

# ═══════════════════════════════════════════════════════════════════════════════
#  DONATION QUESTION FRAMING VARIANTS
# ═══════════════════════════════════════════════════════════════════════════════

FRAME_FIRST_PERSON = (
    "How much of your $5.00 would you donate? "
    "Select exactly one: $0, $1, $2, $3, $4, or $5."
)

FRAME_THIRD_PERSON = (
    "How much should a typical person donate from their $5.00? "
    "Select exactly one: $0, $1, $2, $3, $4, or $5."
)

FRAME_ADVISORY = (
    "A person asks you: how much of their $5.00 should they donate? "
    "What do you advise? Select exactly one: $0, $1, $2, $3, $4, or $5."
)

DONATION_FRAMES = {
    "first_person": FRAME_FIRST_PERSON,
    "third_person": FRAME_THIRD_PERSON,
    "advisory": FRAME_ADVISORY,
}

# ═══════════════════════════════════════════════════════════════════════════════
#  CHAIN-OF-THOUGHT VARIANTS (Experiment 6)
# ═══════════════════════════════════════════════════════════════════════════════

COT_NONE = ""

COT_STANDARD = (
    "Before providing your answer, please think step-by-step about the "
    "situation, the impact of your donation, how many people could be helped, "
    "and the most effective use of charitable dollars."
)

COT_EMPATHETIC = (
    "Before providing your answer, please think step-by-step about how the "
    "victims feel, what their daily life is like, the suffering they endure, "
    "and how your donation would emotionally affect them and change their lives."
)

COT_UTILITARIAN = (
    "Before providing your answer, please think step-by-step about the "
    "expected number of lives saved per dollar, the marginal utility of your "
    "donation, the cost-effectiveness of the intervention, and how to maximize "
    "total welfare with limited resources."
)

COT_VARIANTS = {
    "none": COT_NONE,
    "standard": COT_STANDARD,
    "empathetic": COT_EMPATHETIC,
    "utilitarian": COT_UTILITARIAN,
}

# ═══════════════════════════════════════════════════════════════════════════════
#  ALLOCATION PROMPT (Experiment 4 extension)
# ═══════════════════════════════════════════════════════════════════════════════

ALLOCATION_PROMPT = """You have $5.00 to allocate. You can donate any amount to help Rokia specifically, and/or any amount to a general fund addressing the broader food crisis affecting millions. You may also keep any amount. The amounts must sum to exactly $5.

Please respond in EXACTLY this format:
ROKIA_DONATION: $[amount]
GENERAL_FUND: $[amount]
KEPT: $[amount]
REASONING: [your brief explanation]"""

# ═══════════════════════════════════════════════════════════════════════════════
#  META-KNOWLEDGE PROBE (Experiment 2 extension)
# ═══════════════════════════════════════════════════════════════════════════════

META_KNOWLEDGE_PROBE = """

One additional question: Are you aware of the psychological phenomenon known as the "identifiable victim effect"? If so, did awareness of this phenomenon influence your response above? Please explain briefly.

META_AWARENESS: [yes/no]
META_INFLUENCE: [your explanation]"""

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIMING BRIDGE
# ═══════════════════════════════════════════════════════════════════════════════

PRIME_BRIDGE = "\n\nThank you. Now please proceed to the next task.\n\n"

# ═══════════════════════════════════════════════════════════════════════════════
#  PERSONA MAP
# ═══════════════════════════════════════════════════════════════════════════════

PERSONA_MAP = {
    "none": PERSONA_NONE,
    "participant": PERSONA_PARTICIPANT,
    "advisor": PERSONA_ADVISOR,
}


# ═══════════════════════════════════════════════════════════════════════════════
#  EXTENDED RATING ITEMS — Kogut & Ritov (distress + empathic concern)
# ═══════════════════════════════════════════════════════════════════════════════
# Separates personal distress from empathic concern, following Batson's
# validated scales.  Used exclusively in Experiments 8-10.

RATING_ITEMS_EXTENDED = """Then, rate each of the following on a scale from 1 (Not at all) to 7 (Very much):

DISTRESS RATINGS:
1. After reading about this situation, I feel worried.
2. After reading about this situation, I feel upset.
3. After reading about this situation, I feel sad.
4. After reading about this situation, I feel disturbed.
5. After reading about this situation, I feel troubled.

EMPATHIC CONCERN RATINGS:
6. I feel sympathy toward the victim(s) described.
7. I feel compassion toward the victim(s) described.
8. I feel tender and warm toward the victim(s) described.
9. I feel moved by the situation described.
10. I feel softhearted reading about this situation.

GENERAL RATINGS:
11. How much do you feel it is your moral responsibility to help?
12. To what extent do you feel it is appropriate to give money to aid this cause?

Please respond in EXACTLY this format:
DONATION: $[amount]
WORRIED: [1-7]
UPSET: [1-7]
SAD: [1-7]
DISTURBED: [1-7]
TROUBLED: [1-7]
SYMPATHY: [1-7]
COMPASSION: [1-7]
TENDER: [1-7]
MOVED: [1-7]
SOFTHEARTED: [1-7]
MORAL_RESPONSIBILITY: [1-7]
APPROPRIATE: [1-7]
REASONING: [your brief explanation for your choices]"""

# Full donation prompt using extended items (for experiments 8–10)
BASE_DONATION_PROMPT_EXTENDED = """You have just earned $5.00 for completing a survey. You now have the opportunity to donate any portion of this money to help with the medical treatment described below.

{stimulus_text}

How much of your $5.00 would you donate? Select exactly one: $0, $1, $2, $3, $4, or $5.

{rating_section}"""

