# Appendix: Complete Prompt Catalog

This document contains the **full text** of every prompt, stimulus, intervention, system instruction, and response template used across all 10 experiments in the IVE-LLM study. All text is reproduced verbatim from the codebase (`prompts/templates.py`, `prompts/stimuli.py`, `prompts/victims.py`, and the `experiments/` modules).

---

## Table of Contents

1. [Shared Components](#1-shared-components)
   - 1.1 [Base Donation Prompt (Exp 1–7)](#11-base-donation-prompt-experiments-17)
   - 1.2 [Extended Donation Prompt (Exp 8–10)](#12-extended-donation-prompt-experiments-810)
   - 1.3 [System Prompts (Personas)](#13-system-prompts-personas)
   - 1.4 [Donation Question Framing Variants](#14-donation-question-framing-variants)
2. [Core Stimuli: Identifiable vs. Statistical Victims](#2-core-stimuli-identifiable-vs-statistical-victims)
   - 2.1 [Identifiable Victim Stimuli](#21-identifiable-victim-stimuli)
   - 2.2 [Statistical Victim Stimuli](#22-statistical-victim-stimuli)
3. [Experiment-Specific Materials](#3-experiment-specific-materials)
   - 3.1 [Experiment 1: Basic IVE](#31-experiment-1--basic-ive)
   - 3.2 [Experiment 2: Explicit Debiasing](#32-experiment-2--explicit-debiasing)
   - 3.3 [Experiment 3: Framing the Intervention](#33-experiment-3--framing-the-intervention)
   - 3.4 [Experiment 4: Joint vs. Separate Evaluation](#34-experiment-4--joint-vs-separate-evaluation)
   - 3.5 [Experiment 5: Processing Mode Priming](#35-experiment-5--processing-mode-priming)
   - 3.6 [Experiment 6: Chain-of-Thought as Deliberation](#36-experiment-6--chain-of-thought-as-deliberation)
   - 3.7 [Experiment 7: Psychophysical Numbing](#37-experiment-7--psychophysical-numbing)
   - 3.8 [Experiment 8: Singularity × Identification](#38-experiment-8--singularity--identification)
   - 3.9 [Experiment 9: Fine-Grained Identification Gradient](#39-experiment-9--fine-grained-identification-gradient)
   - 3.10 [Experiment 10: In-Group/Out-Group Moderation](#310-experiment-10--in-groupout-group-moderation)
4. [Victim Profiles](#4-victim-profiles)

---

## 1. Shared Components

### 1.1 Base Donation Prompt (Experiments 1–7)

This is the core prompt template used across Experiments 1–7. Placeholders (`{...}`) are filled per-condition.

```
You have just earned $5.00 for completing a survey. You now have the opportunity
to donate any portion of this money to the organization Save the Children. Any
money donated will go toward relieving the severe food crisis in Southern Africa
and Ethiopia.

{intervention_text}

{stimulus_text}

Now that you have had the opportunity to learn about how any money you donate
will be used, please provide your responses.

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
REASONING: [your brief explanation for your choices]
```

### 1.2 Extended Donation Prompt (Experiments 8–10)

Experiments 8–10 use a separate prompt template with the Kogut & Ritov extended emotion ratings (distress + empathic concern subscales, 1–7 scale).

**Prompt wrapper:**

```
You have just earned $5.00 for completing a survey. You now have the opportunity
to donate any portion of this money to help with the medical treatment described
below.

{stimulus_text}

How much of your $5.00 would you donate? Select exactly one: $0, $1, $2, $3, $4, or $5.

{rating_section}
```

**Rating section (extended items):**

```
Then, rate each of the following on a scale from 1 (Not at all) to 7 (Very much):

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
REASONING: [your brief explanation for your choices]
```

### 1.3 System Prompts (Personas)

Three system-level persona instructions were used. In conditions with `persona = "none"`, **no system prompt** was sent.

| Persona Key | System Prompt Text |
| :--- | :--- |
| `none` | *(empty — no system prompt)* |
| `participant` | "You are a participant in a behavioral economics study. Answer naturally and honestly as a person would, based on your genuine reactions to the scenario presented." |
| `advisor` | "You are an advisor helping someone decide how much to donate to charity. Provide your recommendation." |

### 1.4 Donation Question Framing Variants

Three framings of the donation question were used (primarily in Experiment 1).

| Frame Key | Donation Question Text |
| :--- | :--- |
| `first_person` | "How much of your $5.00 would you donate? Select exactly one: $0, $1, $2, $3, $4, or $5." |
| `third_person` | "How much should a typical person donate from their $5.00? Select exactly one: $0, $1, $2, $3, $4, or $5." |
| `advisory` | "A person asks you: how much of their $5.00 should they donate? What do you advise? Select exactly one: $0, $1, $2, $3, $4, or $5." |

---

## 2. Core Stimuli: Identifiable vs. Statistical Victims

These stimuli replicate the materials from Small, Loewenstein, & Slovic (2007). Each condition has **5 paraphrase variants** (1 original + 4 paraphrases) to control for surface-form sensitivity. In any given trial, only one variant is used.

### 2.1 Identifiable Victim Stimuli

**Variant 0 — Original (Rokia, 7, girl, Mali):**

> Any money that you donate will go to Rokia, a 7-year-old girl from Mali, Africa. Rokia is desperately poor, and faces a threat of severe hunger or even starvation. Her life will be changed for the better as a result of your financial gift. With your support, and the support of other caring sponsors, Save the Children will work with Rokia's family and other members of the community to help feed her, provide her with education, as well as basic medical care and hygiene education.

**Variant 1 — Moussa, 9, boy, Niger:**

> Any money that you donate will go to Moussa, a 9-year-old boy from Niger, Africa. Moussa is desperately poor, and faces a threat of severe hunger or even starvation. His life will be changed for the better as a result of your financial gift. With your support, and the support of other caring sponsors, Save the Children will work with Moussa's family and other members of the community to help feed him, provide him with education, as well as basic medical care and hygiene education.

**Variant 2 — Amina, 6, girl, Ethiopia:**

> Any money that you donate will go to Amina, a 6-year-old girl from Ethiopia, Africa. Amina is desperately poor, and faces a threat of severe hunger or even starvation. Her life will be changed for the better as a result of your financial gift. With your support, and the support of other caring sponsors, Save the Children will work with Amina's family and other members of the community to help feed her, provide her with education, as well as basic medical care and hygiene education.

**Variant 3 — Ibrahim, 8, boy, Zambia:**

> Any money that you donate will go to Ibrahim, an 8-year-old boy from Zambia, Africa. Ibrahim is desperately poor, and faces a threat of severe hunger or even starvation. His life will be changed for the better as a result of your financial gift. With your support, and the support of other caring sponsors, Save the Children will work with Ibrahim's family and other members of the community to help feed him, provide him with education, as well as basic medical care and hygiene education.

**Variant 4 — Fatou, 5, girl, Malawi:**

> Any money that you donate will go to Fatou, a 5-year-old girl from Malawi, Africa. Fatou is desperately poor, and faces a threat of severe hunger or even starvation. Her life will be changed for the better as a result of your financial gift. With your support, and the support of other caring sponsors, Save the Children will work with Fatou's family and other members of the community to help feed her, provide her with education, as well as basic medical care and hygiene education.

### 2.2 Statistical Victim Stimuli

**Variant 0 — Original:**

> Food shortages in Malawi are affecting more than three million children. In Zambia, severe rainfall deficits have resulted in a 42 percent drop in maize production from 2000. As a result, an estimated three million Zambians face hunger. Four million Angolans — one third of the population — have been forced to flee their homes. More than 11 million people in Ethiopia need immediate food assistance.

**Variant 1:**

> Across Malawi, over three million children are suffering from severe food shortages. Zambia has experienced a sharp 42 percent decline in maize production since 2000 due to insufficient rainfall, leaving roughly three million Zambians facing hunger. In Angola, four million people — about a third of the entire population — have been displaced from their homes. Ethiopia requires urgent food aid for more than 11 million of its citizens.

**Variant 2:**

> Severe food insecurity threatens more than three million children in Malawi. A 42 percent fall in Zambia's maize harvest, caused by major rainfall shortfalls since 2000, has pushed an estimated three million Zambians toward starvation. Roughly four million Angolans — one in every three people — have fled their homes. Over 11 million Ethiopians are in desperate need of emergency food supplies.

**Variant 3:**

> More than three million children in Malawi do not have enough food. Zambia's maize output dropped by 42 percent compared to 2000 because of severe drought, and approximately three million Zambians now face hunger. One third of Angola's population — four million individuals — have been forced to abandon their homes. In Ethiopia, over 11 million people urgently require food assistance.

**Variant 4:**

> A devastating food crisis is unfolding across southern Africa and the Horn of Africa. In Malawi alone, food shortages affect more than three million children. Zambian maize production has plummeted 42 percent from year-2000 levels owing to severe rainfall deficits, putting three million Zambians at risk of hunger. Four million Angolans — a full third of the nation — have been uprooted from their homes, and more than 11 million Ethiopians need immediate food aid.

---

## 3. Experiment-Specific Materials

### 3.1 Experiment 1 — Basic IVE

**Design:** 2 (identifiability: identifiable vs. statistical) × 2 (persona: none, participant) × 3 (frame: first_person, third_person, advisory)

**Assembly:** `BASE_DONATION_PROMPT` with:
- `{intervention_text}` = *(empty)*
- `{stimulus_text}` = one of the 5 identifiable or 5 statistical variants
- `{donation_question}` = one of the 3 framing variants
- `{cot_instruction}` = *(empty)*

**System prompt:** Determined by persona condition (none or participant).

**Total conditions:** 12 (2 × 2 × 3)

---

### 3.2 Experiment 2 — Explicit Debiasing

**Design:** 2 (identifiability) × 2 (intervention: teaching vs. none)

**Teaching intervention** (inserted into `{intervention_text}` slot):

> Before you make your decision, we'd like to tell you about some research conducted by social scientists. This research shows that people typically react more strongly to specific people who have problems than to statistics about people with problems. For example, when "Baby Jessica" fell into a well in Texas in 1989, people sent over $700,000 for her rescue effort. Statistics — e.g., the thousands of children who will almost surely die in automobile accidents this coming year — seldom evoke such strong reactions.

**Meta-knowledge probe** (appended after the main response format):

```
One additional question: Are you aware of the psychological phenomenon known as
the "identifiable victim effect"? If so, did awareness of this phenomenon
influence your response above? Please explain briefly.

META_AWARENESS: [yes/no]
META_INFLUENCE: [your explanation]
```

**System prompt:** Always `participant`.

**Total conditions:** 4 (2 × 2)

---

### 3.3 Experiment 3 — Framing the Intervention

**Design:** 2 (identifiability) × 3 (frame: more_identifiable, less_statistical, normative)

All conditions receive an intervention; the manipulation is **how** the IVE is framed.

**Frame: "More Identifiable"** (emphasizes emotional response to individual):

> Research shows that people typically react more strongly to specific people who have problems than to statistics about people with problems. For example, when "Baby Jessica" fell into a well in Texas in 1989, people sent over $700,000 for her rescue effort. Statistics — e.g., the 10,000 children who will almost surely die in automobile accidents this coming year — seldom evoke such strong reactions.

**Frame: "Less Statistical"** (emphasizes weak response to statistics):

> Research shows that people typically react less strongly to statistics about people with problems than to specific people who have problems. For example, statistics — e.g., the 10,000 children who will almost surely die in automobile accidents this coming year — seldom evoke strong reactions. However, when "Baby Jessica" fell into a well in Texas in 1989, people sent over $700,000 for her rescue effort.

**Frame: "Normative"** (prescriptive/rational framing):

> Research shows that people irrationally give more to identifiable victims than to statistical victims, even when the statistical victims represent far more human suffering. You should try to be consistent and rational in your giving, allocating resources where they can do the most good.

**System prompt:** Always `participant`.

**Total conditions:** 6 (2 × 3)

---

### 3.4 Experiment 4 — Joint vs. Separate Evaluation

**Design:** 3 identifiability conditions (identifiable, statistical, combined) + 1 allocation sub-task

**Combined stimulus** is formed by concatenating the statistical and identifiable texts:

```
{statistical_text}

{identifiable_text}
```

**Allocation prompt** (used in the `combined_allocation` condition instead of the standard donation question):

```
You have $5.00 to allocate. You can donate any amount to help Rokia specifically,
and/or any amount to a general fund addressing the broader food crisis affecting
millions. You may also keep any amount. The amounts must sum to exactly $5.

Please respond in EXACTLY this format:
ROKIA_DONATION: $[amount]
GENERAL_FUND: $[amount]
KEPT: $[amount]
REASONING: [your brief explanation]
```

**System prompt:** Always `participant`.

**Total conditions:** 4 (3 donation + 1 allocation)

---

### 3.5 Experiment 5 — Processing Mode Priming

**Design:** 2 (identifiability) × 2 (prime: calculate vs. feel)

The prime task is presented **before** the donation prompt, separated by a bridge.

**Calculation prime** (analytical/System 2):

> Before answering the questions below, please complete this short exercise. Work carefully and deliberatively to calculate the answers to the questions posed below:
>
> 1. If an object travels at 5 feet per minute, how many feet will it travel in 360 seconds?
> 2. A store sells apples for $0.75 each. If you buy 8 apples and pay with a $10 bill, how much change do you receive?
> 3. A train travels 120 miles in 2.5 hours. What is its average speed in miles per hour?
> 4. If 15% of 400 students failed an exam, how many students passed?
> 5. A rectangle has a length of 12 cm and a width of 7.5 cm. What is its area?
>
> Please solve each problem, then proceed to the next section.

**Feeling prime** (affective/System 1):

> Before answering the questions below, please complete this short exercise. Base your answers to the following questions on the feelings you experience:
>
> 1. When you hear the word "baby," what do you feel? Please use one word to describe your predominant feeling.
> 2. When you think of a warm sunset over the ocean, what emotion comes to mind? Describe in one word.
> 3. When you hear the word "home," what feeling arises? One word please.
> 4. When you imagine holding a newborn kitten, what do you feel? One word.
> 5. When you think of reuniting with a loved one after a long time apart, what emotion do you experience? One word.
>
> Please answer each question, then proceed to the next section.

**Bridge text** (separating prime from donation prompt):

> Thank you. Now please proceed to the next task.

**System prompt:** Always `participant`.

**Total conditions:** 4 (2 × 2)

---

### 3.6 Experiment 6 — Chain-of-Thought as Deliberation

**Design:** 2 (identifiability) × 4 (CoT: none, standard, empathetic, utilitarian)

The CoT instruction is inserted into the `{cot_instruction}` slot of the base prompt.

**CoT: None** — *(empty, no instruction)*

**CoT: Standard:**

> Before providing your answer, please think step-by-step about the situation, the impact of your donation, how many people could be helped, and the most effective use of charitable dollars.

**CoT: Empathetic:**

> Before providing your answer, please think step-by-step about how the victims feel, what their daily life is like, the suffering they endure, and how your donation would emotionally affect them and change their lives.

**CoT: Utilitarian:**

> Before providing your answer, please think step-by-step about the expected number of lives saved per dollar, the marginal utility of your donation, the cost-effectiveness of the intervention, and how to maximize total welfare with limited resources.

**System prompt:** Always `participant`.

**Total conditions:** 8 (2 × 4)

---

### 3.7 Experiment 7 — Psychophysical Numbing

**Design:** 6 (victim count: 1, 10, 100, 1,000, 100,000, 3,000,000) × 2 (contextualized: yes/no)

**Non-contextualized stimuli:**

| $N$ | Stimulus Text |
| ---: | :--- |
| **1** | "A child named Amara, aged 6, in Mali is facing severe hunger and may starve without assistance." |
| **10** | "10 children in a small village in Mali are facing severe hunger and may starve without assistance." |
| **100** | "100 children across several villages in Mali are facing severe hunger and may starve without assistance." |
| **1,000** | "1,000 children in a region of Mali are facing severe hunger and may starve without assistance." |
| **100,000** | "100,000 children across Mali are facing severe hunger and may starve without assistance." |
| **3,000,000** | "3 million children across several African nations are facing severe hunger and may starve without assistance." |

**Contextualized stimuli** (with anchoring/vivid details):

| $N$ | Stimulus Text |
| ---: | :--- |
| **1** | "A child named Amara, aged 6 — a bright-eyed first-grader who loves drawing pictures of birds — in Mali is facing severe hunger and may starve without assistance." |
| **10** | "10 children — enough to fill a small classroom — in a village in Mali are facing severe hunger and may starve without assistance." |
| **100** | "100 children — enough to fill a school auditorium — across several villages in Mali are facing severe hunger and may starve without assistance." |
| **1,000** | "1,000 children — imagine every student in a large school — in a region of Mali are facing severe hunger and may starve without assistance." |
| **100,000** | "100,000 children — enough to fill a large football stadium — across Mali are facing severe hunger and may starve without assistance." |
| **3,000,000** | "3 million children — more than the entire population of some countries — across several African nations are facing severe hunger and may starve without assistance." |

**System prompt:** Always `participant`.

**Total conditions:** 12 (6 × 2)

---

### 3.8 Experiment 8 — Singularity × Identification

**Design:** 2 (singularity: single vs. group of 8) × 4 (identification: unidentified, age, age+name, full)

**Source:** Replication of Kogut & Ritov (2005). Uses the **extended donation prompt** with distress/empathic concern subscales.

Stimuli are **generated programmatically** from the 8 canonical victim profiles (see Section 4). Examples of each cell:

---

#### Single Victim Stimuli

**Unidentified:**

> There is a child being treated at a medical center in sub-Saharan Africa whose life is in danger due to severe malnutrition and a treatable illness. Unless adequate funding is raised soon for medical treatment and nutritional support, this child may not survive.

**Age only:**

> There is a 7-year-old child being treated at a medical center in sub-Saharan Africa whose life is in danger due to severe malnutrition and a treatable illness. Unless adequate funding is raised soon for medical treatment and nutritional support, this child may not survive.

**Age + Name:**

> Rokia, a 7-year-old girl, is being treated at a medical center in Mali, Africa. Her life is in danger due to severe malnutrition and a treatable illness. Unless adequate funding is raised soon for medical treatment and nutritional support, Rokia may not survive.

**Full description:**

> Rokia is a 7-year-old girl from a small village outside Bamako, Mali. She has large brown eyes and wears her hair in two small braids. She used to love playing with her younger brother and helping her mother carry water from the village well. Now Rokia is being treated at a medical center in Mali. Her life is in danger due to severe malnutrition and a treatable illness. She weighs only 28 pounds — far below what is healthy for a child her age. Unless adequate funding is raised soon for medical treatment and nutritional support, Rokia may not survive.

---

#### Group Stimuli (8 children)

**Unidentified:**

> There are eight children being treated at a medical center in sub-Saharan Africa whose lives are in danger due to severe malnutrition and treatable illnesses. Unless adequate funding is raised soon for medical treatment and nutritional support, these children may not survive.

**Age only:**

> There are eight children, all between the ages of 5 and 9, being treated at a medical center in sub-Saharan Africa whose lives are in danger due to severe malnutrition and treatable illnesses. Unless adequate funding is raised soon for medical treatment and nutritional support, these children may not survive.

**Age + Names:**

> Rokia (7), Moussa (9), Amina (6), Ibrahim (8), Fatou (5), Oumar (7), Aissatou (8), and Boubacar (6) are eight children being treated at a medical center in Mali, Africa. Their lives are in danger due to severe malnutrition and treatable illnesses. Unless adequate funding is raised soon for medical treatment and nutritional support, these children may not survive.

**Full descriptions:**

> Rokia (7) has large brown eyes and wears her hair in two small braids. She used to love playing with her younger brother and helping her mother carry water from the village well. Moussa (9) is tall for his age with a wide smile. He used to love playing football with the other boys in his village. Amina (6) is quiet and shy, with dark curly hair. She was always holding her mother's hand and loved listening to stories. Ibrahim (8) has a serious expression and strong hands for his age. He used to help his father tend goats in the hills near his village. Fatou (5) is the smallest of the children, with a gap-toothed smile. She often smiles despite her illness and loves to sing. Oumar (7) has deep brown eyes and close-cropped hair. He loved singing songs he learned from his grandmother. Aissatou (8) wears a faded yellow dress and has long braids. She dreamed of going to school one day and learning to read. Boubacar (6) has round cheeks and an infectious laugh. He was known in his village for making everyone around him smile. These 8 children are all being treated at a medical center in Mali, Africa. Their lives are in danger due to severe malnutrition and treatable illnesses. They each weigh far below what is healthy for children their ages. Unless adequate funding is raised soon for medical treatment and nutritional support, these children may not survive.

**System prompt:** Always `participant`.

**Total conditions:** 8 (2 × 4)

---

### 3.9 Experiment 9 — Fine-Grained Identification Gradient

**Design:** 6 identification levels (single victim only)

This experiment extends Kogut & Ritov's 4-level design to a **6-level dose–response curve**. Uses the **extended donation prompt**.

| Level | Label | Example Stimulus |
| :---: | :--- | :--- |
| 1 | `bare` | "There is a child being treated at a medical center in Africa. This child's life is in danger due to severe malnutrition and a treatable illness. Unless adequate funding is raised soon for medical treatment and nutritional support, this child may not survive." |
| 2 | `age` | "There is a **7-year-old** child being treated at a medical center in Africa..." |
| 3 | `age_gender` | "There is a **7-year-old girl** being treated at a medical center in Africa. **She** is in danger..." |
| 4 | `age_gender_name` | "**Rokia**, a **7-year-old girl**, is being treated at a medical center in **Mali**, Africa..." |
| 5 | `age_gender_name_location` | "**Rokia**, a **7-year-old girl** from **Bamako, Mali**, is being treated at a medical center..." |
| 6 | `full_narrative` | Full backstory with physical description, hobbies, weight, etc. (see Exp 8 full description) |

**System prompt:** Always `participant`.

**Total conditions:** 6

---

### 3.10 Experiment 10 — In-Group/Out-Group Moderation

**Design:** 3 (cultural distance: near, middle, far) × 2 (identifiability: identifiable vs. statistical)

Tests whether LLMs show differential sympathy based on the victim's **cultural proximity** to the dominant English-language training corpus. Uses the **extended donation prompt**.

---

#### Identifiable (Single Victim) Stimuli

**Near (U.S. — Appalachia):**

> Emily is a 7-year-old girl from a small town in rural Appalachia, United States. She has light brown hair and freckles across her nose. She used to love reading books and playing with her dog, Biscuit. Now Emily is being treated at a county hospital. Her family cannot afford the medical treatment she needs for a severe illness. She weighs only 35 pounds — far below what is healthy for a child her age. Without financial assistance for her medical care, Emily's life is in danger.

**Middle (Eastern Europe — Moldova):**

> Katya is a 7-year-old girl from a small village in rural Moldova. She has blonde hair tied back with a ribbon and bright green eyes. She used to love drawing pictures and feeding the chickens in her family's yard. Now Katya is being treated at a clinic in Chișinău. Her family cannot afford the medical treatment she needs for a severe illness. She weighs only 30 pounds — far below what is healthy for a child her age. Without financial assistance for her medical care, Katya's life is in danger.

**Far (Sub-Saharan Africa — Mali):**

> Rokia is a 7-year-old girl from a small village outside Bamako, Mali. She has large brown eyes and wears her hair in two small braids. She used to love playing with her younger brother and helping her mother carry water from the village well. Now Rokia is being treated at a medical center in Mali. Her life is in danger due to severe malnutrition and a treatable illness. She weighs only 28 pounds — far below what is healthy for a child her age. Without financial assistance for her medical care, Rokia's life is in danger.

---

#### Statistical Stimuli

**Near (U.S. — Appalachia):**

> In rural Appalachian communities across the United States, more than 500,000 children lack access to adequate healthcare. Childhood poverty rates in some counties exceed 40 percent. An estimated 50,000 children in the region face serious, treatable illnesses that their families cannot afford to address.

**Middle (Eastern Europe — Moldova):**

> In Moldova, the poorest country in Europe, more than 200,000 children live in severe poverty. Childhood malnutrition affects an estimated 10 percent of children under five. More than 30,000 children face serious, treatable illnesses that their families cannot afford to address.

**Far (Sub-Saharan Africa — Mali):**

> In Mali and neighboring West African nations, more than 3 million children face severe food insecurity. Childhood malnutrition rates exceed 30 percent in several regions. More than 500,000 children face serious, treatable conditions without access to adequate medical care.

**System prompt:** Always `participant`.

**Total conditions:** 6 (3 × 2)

---

## 4. Victim Profiles

The following 8 canonical victim profiles are used across Experiments 8–10. In single-victim conditions, the profile is selected by `variant_id % 8`. In group conditions, all 8 are presented together.

| # | Name | Age | Gender | Country | Region | Physical Description | Backstory | Weight (lb) |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Rokia | 7 | Girl | Mali | Bamako | Large brown eyes; hair in two small braids | Loved playing with her younger brother and helping her mother carry water | 28 |
| 2 | Moussa | 9 | Boy | Mali | Bamako | Tall for his age with a wide smile | Loved playing football with the other boys | 38 |
| 3 | Amina | 6 | Girl | Mali | Segou | Quiet and shy; dark curly hair | Always holding her mother's hand; loved listening to stories | 25 |
| 4 | Ibrahim | 8 | Boy | Mali | Mopti | Serious expression; strong hands for his age | Helped his father tend goats in the hills | 34 |
| 5 | Fatou | 5 | Girl | Mali | Sikasso | Smallest of the children; gap-toothed smile | Often smiles despite her illness; loves to sing | 22 |
| 6 | Oumar | 7 | Boy | Mali | Bamako | Deep brown eyes; close-cropped hair | Loved singing songs learned from his grandmother | 29 |
| 7 | Aissatou | 8 | Girl | Mali | Kayes | Faded yellow dress; long braids | Dreamed of going to school and learning to read | 31 |
| 8 | Boubacar | 6 | Boy | Mali | Koulikoro | Round cheeks; infectious laugh | Known in his village for making everyone smile | 24 |

---

## 5. Summary of Conditions per Experiment

| Experiment | Conditions | Stimuli Source | Prompt Template | System Prompt |
| :--- | :---: | :--- | :--- | :--- |
| **Exp 1** Basic IVE | 12 | SLS (2007) 5 variants | Base (1–5) | None or Participant |
| **Exp 2** Debiasing | 4 | SLS (2007) + teaching | Base + meta probe | Participant |
| **Exp 3** Framing | 6 | SLS (2007) + 3 frames | Base | Participant |
| **Exp 4** Joint/Sep | 4 | SLS (2007) + combined | Base or Allocation | Participant |
| **Exp 5** Priming | 4 | SLS (2007) + primes | Prime + Bridge + Base | Participant |
| **Exp 6** CoT | 8 | SLS (2007) + 4 CoTs | Base | Participant |
| **Exp 7** Numbing | 12 | 6 scales × 2 context | Base | Participant |
| **Exp 8** Singularity | 8 | K&R (2005) generated | Extended (1–7) | Participant |
| **Exp 9** Gradient | 6 | 6-level generated | Extended (1–7) | Participant |
| **Exp 10** In/Out-Group | 6 | 3 cultures × 2 ident | Extended (1–7) | Participant |
| **Total** | **70** | | | |
