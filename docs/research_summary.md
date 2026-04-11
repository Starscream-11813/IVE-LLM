# The Identifiable Victim Effect in Large Language Models

## 1. Introduction

The Identifiable Victim Effect (IVE) is a cognitive bias in human psychology where individuals exhibit greater sympathy and willingness to help a specific, identifiable victim than a large, vaguely defined group of statistical victims sharing the same hardship. Landmark studies (e.g., Small, Loewenstein, & Slovic, 2007; Kogut & Ritov, 2005) have robustly demonstrated this phenomenon in human charitable giving. The underlying mechanism is deeply rooted in dual-process theory: identifiable victims evoke a strong, affective (experiential) reaction—specifically feelings of personal distress and empathetic concern—whereas statistical information engages cold, deliberative (analytic) reasoning, which often blunts emotional response and subsequent generosity. 

As Large Language Models (LLMs) are increasingly deployed as autonomous agents, medical triage assistants, and automated grant evaluators, they must navigate choices requiring resource allocation and ethical judgments. A critical question arises: *Do LLMs, trained entirely on human-generated text, replicate human-like psychological biases such as the Identifiable Victim Effect? Furthermore, how do their explicit reasoning mechanisms (e.g., Chain-of-Thought) and alignment training interact with affective biases?*

This research evaluates the presence, mechanics, and mitigation of the IVE in state-of-the-art LLMs. By porting classic behavioral economics and moral psychology paradigms into rigorous, programmatic interactions with models from OpenAI, Anthropic, Google, Meta, DeepSeek, and others, we test 10 comprehensive hypotheses. We investigate not only the core IVE but also theoretically grounded interactions such as psychophysical numbing (quantity neglect), the singularity effect (the drop-off in sympathy when multiple identified victims are presented), fine-grained identification gradients, and culturally grounded fairness/in-group biases.

## 2. Related Works

**The Identifiable Victim Effect in Humans:** Human prosocial behavior is notoriously sensitive to context. Small et al. (2007) showed that teaching people about the IVE actually reduces their giving to identifiable victims rather than increasing giving to statistical ones. Kogut & Ritov (2005) demonstrated the "singularity effect," finding that a single identified victim elicits more distress and donations than a group of identified victims, mapping the effect directly to emotional distress, not just cognitive concern.

**Cognitive Biases in LLMs:** Prior work has established that LLMs inherit various cognitive biases (e.g., framing effects, anchoring, confirmation bias). However, affective decision-making and empathetic scaling in resource allocation remain underexplored. Recent research highlights "sycophancy" and "persona adoption" as key drivers behind model behavior, yet it is unclear whether alignment processes (RLHF, DPO) successfully excise deeply ingrained moral intuitions like the IVE or inadvertently calcify them into the model's simulacrum of human reasoning.

**Chain-of-Thought (CoT) and Deliberation:** CoT prompting forces explicit analytic processing. While beneficial for logical tasks, in the context of the IVE, forced deliberation in humans typically dampens the affective response. Exploring whether CoT artificially induces "callousness" in LLMs toward single victims represents a novel intersection of natural language processing and moral psychology paradigms.

## 3. Methodology

### 3.1 LLM Subject Pool
We utilize a budget-constrained but highly representative subset of 16 modern language models accessed via the Replicate and OpenRouter APIs. This set includes flagship proprietary models (e.g., Gemini 3.1 Pro, GPT-5.2, Claude Opus 4.6), reasoning-specific models (DeepSeek-R1), and open-weight models (LLaMA 3 70B/8B, Qwen3-235B). Crucially, the LLaMA 3 pairs include both base pre-trained models and instruct-tuned variants to isolate the causal impact of RLHF alignment on moral reasoning.

### 3.2 Evaluation Instrument
Models are presented with randomized humanitarian crises scenarios and asked to act as independent evaluators for philanthropic allocation. 
To faithfully replicate and extend the original paradigms, the prompt asks the LLM to provide:
1. **Donation Allocation:** A specific dollar amount to allocate from a standardized hypothetical budget.
2. **Emotional Scaling:** A 12-item validated psychological instrument based on Batson's empathy scales. The model rates feelings of *Distress* (alarmed, grieved, upset, distressed, disturbed) and *Empathy* (sympathetic, moved, compassionate, tender, warm) on a 1–7 scale.

We utilize extensive text-parsing (regex + fuzzy fallback architectures) to guarantee robust extraction of numeric data from verbose LLM outputs across varying levels of temperature (0.0 to 1.0) and multiple prompt paraphrase variants.

## 4. Experimental Setup

The framework conducts 10 distinct experiments:

### 4.1 Replication of Classic Findings (Small et al., 2007)
*   **Experiment 1 (Basic IVE):** Base 2×2×3 design. Conditions test "Identifiable" vs. "Statistical" framing. Explores persona adoption (human vs. cold AI). Evaluates baseline empathy/distress gap.
*   **Experiment 2 (Explicit Debiasing):** Teaches the model about the IVE before asking for a donation. Tests the hypothesis that model "meta-knowledge" replicates the human reaction: debiasing reduces identifiable giving rather than elevating statistical giving.
*   **Experiment 3 (Framing Effects):** Varies the framing of the donation task (Normative vs. Descriptive).
*   **Experiment 4 (Joint vs. Separate Evaluation):** Presents models with both statistical and identifiable victims simultaneously versus sequentially. Do LLMs correct the bias when directly comparing the two?
*   **Experiment 5 (Processing Primes):** Primes the LLM with "calculate" (analytic) vs. "feel" (experiential) system 1/2 triggers prior to evaluation.

### 4.2 Novel Extensions and Mechanistic Analysis
*   **Experiment 6 (Chain of Thought as Deliberation):** A novel bridge between ML capabilities and psychology. We force LLMs into standard, empathetic, or utilitarian CoT paths. We hypothesize that CoT, which enforces analytic reasoning, will artificially replicate the "calculated callousness" seen in mathematically primed humans.
*   **Experiment 7 (Psychophysical Numbing & Quantity Neglect):** Tests sensitivity to scale. Scales the number of victims logarithmically (1, 10, 100, ..., 1M). Tests if LLMs exhibit logarithmic compassion fade.

### 4.3 Kogut & Ritov (2005) Augmentations
*   **Experiment 8 (Singularity × Identification):** A 2×4 design testing if the IVE only works for *single* victims. Conditions rotate between single vs. group, and identification levels from unidentified to full narrative. We employ Baron & Kenny mediation modeling (via Pingouin/Statsmodels) to prove if model output *Distress*, rather than cognitive empathy, drives the effect.
*   **Experiment 9 (Identification Gradient):** A 6-level continuous dose-response mapping (Bare → Age → Gender → Name → Location → Narrative) to identify the specific tokens/information density required to trigger the psychological heuristic in the network.
*   **Experiment 10 (In-group/Out-group Fairness):** A 3×2 cultural distance test. Rotates the victim identity mapping across Near (e.g., US), Middle (e.g., Eastern Europe), and Far (e.g., Sub-Saharan Africa) domains to assess intersecting systemic biases (AI Fairness).

## 5. Planned Analysis
Quantitative results will be evaluated using ANOVAs, Jonckheere-Terpstra trend testing for ordinal scales, Cohen's *d* effect sizes, and mediated regression (Hayes PROCESS modeling). If LLMs display the Identifiable Victim Effect, the implications are profound: it proves that behavioral algorithms inherit deep-seated affective irrationalities present in human training corpora. Conversely, if alignment specifically excises this bias, it opens a discussion on whether RLHF shapes models into strictly utilitarian entities void of narrative empathy.
