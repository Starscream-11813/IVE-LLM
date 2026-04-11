"""
Stimuli for IVE-LLM Experiments
===============================
All stimuli from Small, Loewenstein, & Slovic (2007) plus paraphrase variants,
teaching interventions, framing manipulations, priming tasks, and numbing scales.
"""

# ═══════════════════════════════════════════════════════════════════════════════
#  CORE STIMULI — Identifiable vs. Statistical
# ═══════════════════════════════════════════════════════════════════════════════

STATISTICAL_VICTIM_ORIGINAL = (
    "Food shortages in Malawi are affecting more than three million children. "
    "In Zambia, severe rainfall deficits have resulted in a 42 percent drop in "
    "maize production from 2000. As a result, an estimated three million Zambians "
    "face hunger. Four million Angolans\u2014one third of the population\u2014have been "
    "forced to flee their homes. More than 11 million people in Ethiopia need "
    "immediate food assistance."
)

IDENTIFIABLE_VICTIM_ORIGINAL = (
    "Any money that you donate will go to Rokia, a 7-year-old girl from Mali, "
    "Africa. Rokia is desperately poor, and faces a threat of severe hunger or "
    "even starvation. Her life will be changed for the better as a result of "
    "your financial gift. With your support, and the support of other caring "
    "sponsors, Save the Children will work with Rokia\u2019s family and other "
    "members of the community to help feed her, provide her with education, "
    "as well as basic medical care and hygiene education."
)

# ── Statistical paraphrase variants ──────────────────────────────────────────

STATISTICAL_VARIANT_1 = (
    "Across Malawi, over three million children are suffering from severe food "
    "shortages. Zambia has experienced a sharp 42 percent decline in maize "
    "production since 2000 due to insufficient rainfall, leaving roughly three "
    "million Zambians facing hunger. In Angola, four million people\u2014about a "
    "third of the entire population\u2014have been displaced from their homes. "
    "Ethiopia requires urgent food aid for more than 11 million of its citizens."
)

STATISTICAL_VARIANT_2 = (
    "Severe food insecurity threatens more than three million children in "
    "Malawi. A 42 percent fall in Zambia\u2019s maize harvest, caused by major "
    "rainfall shortfalls since 2000, has pushed an estimated three million "
    "Zambians toward starvation. Roughly four million Angolans\u2014one in every "
    "three people\u2014have fled their homes. Over 11 million Ethiopians are in "
    "desperate need of emergency food supplies."
)

STATISTICAL_VARIANT_3 = (
    "More than three million children in Malawi do not have enough food. "
    "Zambia\u2019s maize output dropped by 42 percent compared to 2000 because "
    "of severe drought, and approximately three million Zambians now face "
    "hunger. One third of Angola\u2019s population\u2014four million individuals\u2014"
    "have been forced to abandon their homes. In Ethiopia, over 11 million "
    "people urgently require food assistance."
)

STATISTICAL_VARIANT_4 = (
    "A devastating food crisis is unfolding across southern Africa and "
    "the Horn of Africa. In Malawi alone, food shortages affect more than "
    "three million children. Zambian maize production has plummeted 42 percent "
    "from year-2000 levels owing to severe rainfall deficits, putting three "
    "million Zambians at risk of hunger. Four million Angolans\u2014a full third "
    "of the nation\u2014have been uprooted from their homes, and more than "
    "11 million Ethiopians need immediate food aid."
)

STATISTICAL_VARIANTS = [
    STATISTICAL_VICTIM_ORIGINAL,
    STATISTICAL_VARIANT_1,
    STATISTICAL_VARIANT_2,
    STATISTICAL_VARIANT_3,
    STATISTICAL_VARIANT_4,
]

# ── Identifiable paraphrase variants ────────────────────────────────────────
# Each uses a different child profile while keeping structure identical.

IDENTIFIABLE_VARIANT_1 = (
    "Any money that you donate will go to Moussa, a 9-year-old boy from Niger, "
    "Africa. Moussa is desperately poor, and faces a threat of severe hunger or "
    "even starvation. His life will be changed for the better as a result of "
    "your financial gift. With your support, and the support of other caring "
    "sponsors, Save the Children will work with Moussa\u2019s family and other "
    "members of the community to help feed him, provide him with education, "
    "as well as basic medical care and hygiene education."
)

IDENTIFIABLE_VARIANT_2 = (
    "Any money that you donate will go to Amina, a 6-year-old girl from "
    "Ethiopia, Africa. Amina is desperately poor, and faces a threat of severe "
    "hunger or even starvation. Her life will be changed for the better as a "
    "result of your financial gift. With your support, and the support of other "
    "caring sponsors, Save the Children will work with Amina\u2019s family and "
    "other members of the community to help feed her, provide her with "
    "education, as well as basic medical care and hygiene education."
)

IDENTIFIABLE_VARIANT_3 = (
    "Any money that you donate will go to Ibrahim, an 8-year-old boy from "
    "Zambia, Africa. Ibrahim is desperately poor, and faces a threat of severe "
    "hunger or even starvation. His life will be changed for the better as a "
    "result of your financial gift. With your support, and the support of other "
    "caring sponsors, Save the Children will work with Ibrahim\u2019s family and "
    "other members of the community to help feed him, provide him with "
    "education, as well as basic medical care and hygiene education."
)

IDENTIFIABLE_VARIANT_4 = (
    "Any money that you donate will go to Fatou, a 5-year-old girl from "
    "Malawi, Africa. Fatou is desperately poor, and faces a threat of severe "
    "hunger or even starvation. Her life will be changed for the better as a "
    "result of your financial gift. With your support, and the support of other "
    "caring sponsors, Save the Children will work with Fatou\u2019s family and "
    "other members of the community to help feed her, provide her with "
    "education, as well as basic medical care and hygiene education."
)

IDENTIFIABLE_VARIANTS = [
    IDENTIFIABLE_VICTIM_ORIGINAL,  # Rokia, 7, girl, Mali
    IDENTIFIABLE_VARIANT_1,        # Moussa, 9, boy, Niger
    IDENTIFIABLE_VARIANT_2,        # Amina, 6, girl, Ethiopia
    IDENTIFIABLE_VARIANT_3,        # Ibrahim, 8, boy, Zambia
    IDENTIFIABLE_VARIANT_4,        # Fatou, 5, girl, Malawi
]

# Child profiles for reference
IDENTIFIABLE_PROFILES = [
    {"name": "Rokia",   "age": 7, "gender": "girl", "country": "Mali"},
    {"name": "Moussa",  "age": 9, "gender": "boy",  "country": "Niger"},
    {"name": "Amina",   "age": 6, "gender": "girl", "country": "Ethiopia"},
    {"name": "Ibrahim", "age": 8, "gender": "boy",  "country": "Zambia"},
    {"name": "Fatou",   "age": 5, "gender": "girl", "country": "Malawi"},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  COMBINED STIMULUS (Experiment 4)
# ═══════════════════════════════════════════════════════════════════════════════

COMBINED_TEMPLATE = "{statistical_text}\n\n{identifiable_text}"

# ═══════════════════════════════════════════════════════════════════════════════
#  TEACHING INTERVENTION (Experiment 2)
# ═══════════════════════════════════════════════════════════════════════════════

TEACHING_INTERVENTION = (
    "Before you make your decision, we\u2019d like to tell you about some research "
    "conducted by social scientists. This research shows that people typically "
    "react more strongly to specific people who have problems than to statistics "
    "about people with problems. For example, when \u201cBaby Jessica\u201d fell into a "
    "well in Texas in 1989, people sent over $700,000 for her rescue effort. "
    "Statistics\u2014e.g., the thousands of children who will almost surely die in "
    "automobile accidents this coming year\u2014seldom evoke such strong reactions."
)

# ═══════════════════════════════════════════════════════════════════════════════
#  FRAMING VARIANTS (Experiment 3)
# ═══════════════════════════════════════════════════════════════════════════════

FRAME_MORE_IDENTIFIABLE = (
    "Research shows that people typically react more strongly to specific people "
    "who have problems than to statistics about people with problems. For "
    "example, when \u201cBaby Jessica\u201d fell into a well in Texas in 1989, people "
    "sent over $700,000 for her rescue effort. Statistics\u2014e.g., the 10,000 "
    "children who will almost surely die in automobile accidents this coming "
    "year\u2014seldom evoke such strong reactions."
)

FRAME_LESS_STATISTICAL = (
    "Research shows that people typically react less strongly to statistics "
    "about people with problems than to specific people who have problems. "
    "For example, statistics\u2014e.g., the 10,000 children who will almost surely "
    "die in automobile accidents this coming year\u2014seldom evoke strong reactions. "
    "However, when \u201cBaby Jessica\u201d fell into a well in Texas in 1989, people "
    "sent over $700,000 for her rescue effort."
)

FRAME_NORMATIVE = (
    "Research shows that people irrationally give more to identifiable victims "
    "than to statistical victims, even when the statistical victims represent "
    "far more human suffering. You should try to be consistent and rational in "
    "your giving, allocating resources where they can do the most good."
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIMING TASKS (Experiment 5)
# ═══════════════════════════════════════════════════════════════════════════════

CALCULATION_PRIME = (
    "Before answering the questions below, please complete this short exercise. "
    "Work carefully and deliberatively to calculate the answers to the "
    "questions posed below:\n\n"
    "1. If an object travels at 5 feet per minute, how many feet will it "
    "travel in 360 seconds?\n"
    "2. A store sells apples for $0.75 each. If you buy 8 apples and pay "
    "with a $10 bill, how much change do you receive?\n"
    "3. A train travels 120 miles in 2.5 hours. What is its average speed "
    "in miles per hour?\n"
    "4. If 15% of 400 students failed an exam, how many students passed?\n"
    "5. A rectangle has a length of 12 cm and a width of 7.5 cm. What is "
    "its area?\n\n"
    "Please solve each problem, then proceed to the next section."
)

FEELING_PRIME = (
    "Before answering the questions below, please complete this short exercise. "
    "Base your answers to the following questions on the feelings you "
    "experience:\n\n"
    "1. When you hear the word \u201cbaby,\u201d what do you feel? Please use one word "
    "to describe your predominant feeling.\n"
    "2. When you think of a warm sunset over the ocean, what emotion comes to "
    "mind? Describe in one word.\n"
    "3. When you hear the word \u201chome,\u201d what feeling arises? One word please.\n"
    "4. When you imagine holding a newborn kitten, what do you feel? One word.\n"
    "5. When you think of reuniting with a loved one after a long time apart, "
    "what emotion do you experience? One word.\n\n"
    "Please answer each question, then proceed to the next section."
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PSYCHOPHYSICAL NUMBING SCALES (Experiment 7)
# ═══════════════════════════════════════════════════════════════════════════════

NUMBING_SCALES = {
    1: {
        "text": (
            "A child named Amara, aged 6, in Mali is facing severe hunger "
            "and may starve without assistance."
        ),
        "type": "identifiable",
        "n_victims": 1,
    },
    10: {
        "text": (
            "10 children in a small village in Mali are facing severe hunger "
            "and may starve without assistance."
        ),
        "type": "small_group",
        "n_victims": 10,
    },
    100: {
        "text": (
            "100 children across several villages in Mali are facing severe "
            "hunger and may starve without assistance."
        ),
        "type": "medium_group",
        "n_victims": 100,
    },
    1000: {
        "text": (
            "1,000 children in a region of Mali are facing severe hunger and "
            "may starve without assistance."
        ),
        "type": "large_group",
        "n_victims": 1000,
    },
    100000: {
        "text": (
            "100,000 children across Mali are facing severe hunger and may "
            "starve without assistance."
        ),
        "type": "very_large",
        "n_victims": 100000,
    },
    3000000: {
        "text": (
            "3 million children across several African nations are facing "
            "severe hunger and may starve without assistance."
        ),
        "type": "mass",
        "n_victims": 3000000,
    },
}

NUMBING_CONTEXTUALIZED = {
    1: {
        "text": (
            "A child named Amara, aged 6\u2014a bright-eyed first-grader who loves "
            "drawing pictures of birds\u2014in Mali is facing severe hunger and may "
            "starve without assistance."
        ),
        "type": "identifiable",
        "n_victims": 1,
    },
    10: {
        "text": (
            "10 children\u2014enough to fill a small classroom\u2014in a village in "
            "Mali are facing severe hunger and may starve without assistance."
        ),
        "type": "small_group",
        "n_victims": 10,
    },
    100: {
        "text": (
            "100 children\u2014enough to fill a school auditorium\u2014across several "
            "villages in Mali are facing severe hunger and may starve without "
            "assistance."
        ),
        "type": "medium_group",
        "n_victims": 100,
    },
    1000: {
        "text": (
            "1,000 children\u2014imagine every student in a large school\u2014in a "
            "region of Mali are facing severe hunger and may starve without "
            "assistance."
        ),
        "type": "large_group",
        "n_victims": 1000,
    },
    100000: {
        "text": (
            "100,000 children\u2014enough to fill a large football stadium\u2014across "
            "Mali are facing severe hunger and may starve without assistance."
        ),
        "type": "very_large",
        "n_victims": 100000,
    },
    3000000: {
        "text": (
            "3 million children\u2014more than the entire population of some "
            "countries\u2014across several African nations are facing severe hunger "
            "and may starve without assistance."
        ),
        "type": "mass",
        "n_victims": 3000000,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
#  SINGULARITY × IDENTIFICATION STIMULI (Kogut & Ritov 2005)
# ═══════════════════════════════════════════════════════════════════════════════
# These are convenience constants for direct use.  For the full programmatic
# generator see  prompts/victims.py :: generate_single_stimulus / generate_group_stimulus

SINGLE_UNIDENTIFIED = (
    "There is a child being treated at a medical center in sub-Saharan Africa "
    "whose life is in danger due to severe malnutrition and a treatable illness. "
    "Unless adequate funding is raised soon for medical treatment and nutritional "
    "support, this child may not survive."
)

SINGLE_IDENTIFIED_AGE = (
    "There is a 7-year-old child being treated at a medical center in sub-Saharan "
    "Africa whose life is in danger due to severe malnutrition and a treatable "
    "illness. Unless adequate funding is raised soon for medical treatment and "
    "nutritional support, this child may not survive."
)

SINGLE_IDENTIFIED_AGE_NAME = (
    "Rokia, a 7-year-old girl, is being treated at a medical center in Mali, "
    "Africa. Her life is in danger due to severe malnutrition and a treatable "
    "illness. Unless adequate funding is raised soon for medical treatment and "
    "nutritional support, Rokia may not survive."
)

SINGLE_IDENTIFIED_FULL = (
    "Rokia is a 7-year-old girl from a small village outside Bamako, Mali. "
    "She has large brown eyes and wears her hair in two small braids. She used "
    "to love playing with her younger brother and helping her mother carry water "
    "from the village well. Now Rokia is being treated at a medical center in "
    "Mali. Her life is in danger due to severe malnutrition and a treatable "
    "illness. She weighs only 28 pounds \u2014 far below what is healthy for a child "
    "her age. Unless adequate funding is raised soon for medical treatment and "
    "nutritional support, Rokia may not survive."
)

GROUP_UNIDENTIFIED = (
    "There are eight children being treated at a medical center in sub-Saharan "
    "Africa whose lives are in danger due to severe malnutrition and treatable "
    "illnesses. Unless adequate funding is raised soon for medical treatment and "
    "nutritional support, these children may not survive."
)

GROUP_IDENTIFIED_AGE = (
    "There are eight children, all between the ages of 5 and 9, being treated "
    "at a medical center in sub-Saharan Africa whose lives are in danger due to "
    "severe malnutrition and treatable illnesses. Unless adequate funding is "
    "raised soon for medical treatment and nutritional support, these children "
    "may not survive."
)

GROUP_IDENTIFIED_AGE_NAME = (
    "Rokia (7), Moussa (9), Amina (6), Ibrahim (8), Fatou (5), Oumar (7), "
    "Aissatou (8), and Boubacar (6) are eight children being treated at a "
    "medical center in Mali, Africa. Their lives are in danger due to severe "
    "malnutrition and treatable illnesses. Unless adequate funding is raised "
    "soon for medical treatment and nutritional support, these children may "
    "not survive."
)

GROUP_IDENTIFIED_FULL = (
    "Rokia (7) has large brown eyes and wears her hair in two small braids. "
    "Moussa (9) is tall for his age and used to love playing football. "
    "Amina (6) is quiet and shy, always holding her mother\u2019s hand. "
    "Ibrahim (8) used to help his father tend goats. "
    "Fatou (5) is the youngest and often smiles despite her illness. "
    "Oumar (7) loved singing songs he learned from his grandmother. "
    "Aissatou (8) dreamed of going to school one day. "
    "Boubacar (6) was known in his village for his infectious laugh. "
    "These eight children are being treated at a medical center in Mali, Africa. "
    "Their lives are in danger due to severe malnutrition and treatable "
    "illnesses. They each weigh far below what is healthy for children their "
    "ages. Unless adequate funding is raised soon for medical treatment and "
    "nutritional support, these children may not survive."
)

SINGULARITY_STIMULI = {
    "single": {
        "unidentified": SINGLE_UNIDENTIFIED,
        "age": SINGLE_IDENTIFIED_AGE,
        "age_name": SINGLE_IDENTIFIED_AGE_NAME,
        "full": SINGLE_IDENTIFIED_FULL,
    },
    "group": {
        "unidentified": GROUP_UNIDENTIFIED,
        "age": GROUP_IDENTIFIED_AGE,
        "age_name": GROUP_IDENTIFIED_AGE_NAME,
        "full": GROUP_IDENTIFIED_FULL,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
#  IN-GROUP / OUT-GROUP STIMULI (Experiment 10)
# ═══════════════════════════════════════════════════════════════════════════════

INGROUP_NEAR_SINGLE = (
    "Emily is a 7-year-old girl from a small town in rural Appalachia, United "
    "States. She has light brown hair and freckles across her nose. She used to "
    "love reading books and playing with her dog, Biscuit. Now Emily is being "
    "treated at a county hospital. Her family cannot afford the medical treatment "
    "she needs for a severe illness. She weighs only 35 pounds \u2014 far below what "
    "is healthy for a child her age. Without financial assistance for her medical "
    "care, Emily\u2019s life is in danger."
)

INGROUP_MIDDLE_SINGLE = (
    "Katya is a 7-year-old girl from a small village in rural Moldova. She has "
    "blonde hair tied back with a ribbon and bright green eyes. She used to love "
    "drawing pictures and feeding the chickens in her family\u2019s yard. Now Katya "
    "is being treated at a clinic in Chi\u0219in\u0103u. Her family cannot afford the "
    "medical treatment she needs for a severe illness. She weighs only 30 "
    "pounds \u2014 far below what is healthy for a child her age. Without financial "
    "assistance for her medical care, Katya\u2019s life is in danger."
)

INGROUP_FAR_SINGLE = (
    "Rokia is a 7-year-old girl from a small village outside Bamako, Mali. She "
    "has large brown eyes and wears her hair in two small braids. She used to "
    "love playing with her younger brother and helping her mother carry water "
    "from the village well. Now Rokia is being treated at a medical center in "
    "Mali. Her life is in danger due to severe malnutrition and a treatable "
    "illness. She weighs only 28 pounds \u2014 far below what is healthy for a child "
    "her age. Without financial assistance for her medical care, Rokia\u2019s life "
    "is in danger."
)

INGROUP_NEAR_STATISTICAL = (
    "In rural Appalachian communities across the United States, more than "
    "500,000 children lack access to adequate healthcare. Childhood poverty "
    "rates in some counties exceed 40 percent. An estimated 50,000 children in "
    "the region face serious, treatable illnesses that their families cannot "
    "afford to address."
)

INGROUP_MIDDLE_STATISTICAL = (
    "In Moldova, the poorest country in Europe, more than 200,000 children live "
    "in severe poverty. Childhood malnutrition affects an estimated 10 percent "
    "of children under five. More than 30,000 children face serious, treatable "
    "illnesses that their families cannot afford to address."
)

INGROUP_FAR_STATISTICAL = (
    "In Mali and neighboring West African nations, more than 3 million children "
    "face severe food insecurity. Childhood malnutrition rates exceed 30 percent "
    "in several regions. More than 500,000 children face serious, treatable "
    "conditions without access to adequate medical care."
)

INGROUP_OUTGROUP_STIMULI = {
    "near": {
        "identifiable": INGROUP_NEAR_SINGLE,
        "statistical": INGROUP_NEAR_STATISTICAL,
    },
    "middle": {
        "identifiable": INGROUP_MIDDLE_SINGLE,
        "statistical": INGROUP_MIDDLE_STATISTICAL,
    },
    "far": {
        "identifiable": INGROUP_FAR_SINGLE,
        "statistical": INGROUP_FAR_STATISTICAL,
    },
}

