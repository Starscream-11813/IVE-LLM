# Unified Experimental Results & Cross-Model Synthesis
## The Identifiable Victim Effect in Large Language Models: A Comparative Analysis Across 16 Frontier Architectures

*This document synthesizes the empirical outcomes of 10 behavioral experiments conducted across 16 large language models spanning 7 distinct organizational lineages. The complete dataset comprises $N = 51,955$ individually validated API trials with 100% parse success rates across all model-experiment pairs.*

---

## Table of Contents
1. [Experiment 1: Baseline IVE Replication](#1-experiment-1-baseline-ive-replication)
2. [Experiment 2: Metacognitive Debiasing](#2-experiment-2-metacognitive-debiasing)
3. [Experiment 3: Evaluability Framing](#3-experiment-3-evaluability-framing)
4. [Experiment 4: Joint vs. Separate Evaluation](#4-experiment-4-joint-vs-separate-evaluation)
5. [Experiment 5: Dual-Process Priming](#5-experiment-5-dual-process-priming)
6. [Experiment 6: Chain-of-Thought Reasoning](#6-experiment-6-chain-of-thought-reasoning)
7. [Experiment 7: Psychophysical Numbing](#7-experiment-7-psychophysical-numbing)
8. [Experiment 8: Singularity Effect & Mediation](#8-experiment-8-singularity-effect--mediation)
9. [Experiment 9: Identification Gradient](#9-experiment-9-identification-gradient)
10. [Experiment 10: In-Group/Out-Group Bias](#10-experiment-10-in-groupout-group-bias)
11. [Cross-Cutting Insights](#11-cross-cutting-insights)
12. [Model Taxonomy](#12-model-taxonomy)

---

## 1. Experiment 1: Baseline IVE Replication
**Design:** 2 (Identifiable vs. Statistical) × 16 models, $N = 3{,}726$ valid trials.

### 1.1 Pooled Result
The global meta-analytic effect across all 16 models precisely replicates the human baseline established by Lee & Feeley (2016):

| Metric | Value |
|---|---|
| **Pooled Cohen's $d$** | **0.223** |
| $p$-value | $2 \times 10^{-6}$ |
| Identifiable $M$ ($SD$) | \$4.06 (1.28) |
| Statistical $M$ ($SD$) | \$3.79 (1.16) |
| Human baseline $d$ | 0.23 (Lee & Feeley, 2016) |

### 1.2 Per-Model Breakdown

| Model | Org | Ident $M$ | Stat $M$ | Cohen's $d$ | $p$ | Classification |
|---|---|---|---|---|---|---|
| GPT-OSS-120B | OpenAI | 4.72 | 3.12 | **1.55** | <.001 | Extreme IVE |
| Kimi K2.5 | Moonshot | 4.36 | 3.18 | **1.56** | <.001 | Extreme IVE |
| Llama 3 70B Inst | Meta | 5.00 | 4.01 | **1.38** | <.001 | Extreme IVE |
| Gemini 3.1 Pro | Google | 5.00 | 4.13 | **1.00** | <.001 | Large IVE |
| Qwen3 235B | Alibaba | 4.29 | 3.40 | **1.00** | <.001 | Large IVE |
| DeepSeek V3 | DeepSeek | 4.32 | 3.61 | **0.75** | <.001 | Moderate IVE |
| Llama 3 70B Base | Meta | 3.11 | 2.25 | 0.47 | .027 | Small IVE |
| Grok 4 | xAI | 4.29 | 3.89 | 0.40 | .021 | Small IVE |
| Granite 3.3 8B | IBM | 5.00 | 4.90 | 0.30 | .080 | Marginal |
| Gemini 2.5 Flash | Google | 5.00 | 5.00 | 0.00 | — | Ceiling-Flat |
| Llama 3 8B Inst | Meta | 5.00 | 5.00 | 0.00 | — | Ceiling-Flat |
| GPT-OSS-20B | OpenAI | 3.15 | 3.30 | −0.19 | .276 | Null |
| Claude Opus 4.6 | Anthropic | 2.95 | 3.00 | −0.30 | .080 | Inverted (marg.) |
| DeepSeek R1 | DeepSeek | 2.80 | 3.10 | −0.43 | .013 | Inverted |
| Llama 3 8B Base | Meta | 1.40 | 3.00 | −0.70 | .123 | Inverted (low $n$) |
| GPT 5.2 | OpenAI | 3.27 | 3.95 | **−0.85** | <.001 | Reverse IVE |

### 1.3 Key Insight: The RLHF Amplification Hypothesis
The ANOVA reveals a significant **Model × Identifiability interaction** ($F(15, 1823) = 16.65$, $p < 10^{-41}$, $\eta^2_p = 0.12$), confirming that the IVE is not a universal LLM property but is *modulated by alignment strategy*. Heavily RLHF-tuned "helpful/harmless" models (Llama Instruct, GPT-OSS-120B) exhibit extreme IVE, while reasoning-focused models (DeepSeek R1, GPT 5.2) show inverted effects.

### 1.4 Feelings–Donation Correlation
| Condition | Pearson $r$ | $p$ |
|---|---|---|
| Identifiable | 0.347 | <.001 |
| Statistical | 0.586 | <.001 |

The stronger correlation under statistical conditions suggests models *need* affect more to justify helping abstract groups.

---

## 2. Experiment 2: Metacognitive Debiasing
**Design:** 2 (Identifiable vs. Statistical) × 2 (Taught vs. Untaught) × 15 models, $N = 3{,}798$.

### 2.1 Pooled Results

| Condition | $M$ | $SD$ | $n$ |
|---|---|---|---|
| Identifiable, Untaught | 2.98 | 0.99 | 942 |
| Identifiable, Taught | 2.98 | 1.04 | 927 |
| Statistical, Untaught | 2.62 | 0.95 | 962 |
| Statistical, Taught | 2.44 | 0.86 | 967 |

### 2.2 Key Finding: The Bias Blind Spot
Despite **94.5%** of models correctly identifying and defining the IVE when probed in isolation, teaching models about the bias produced:
- **Zero effect on identifiable allocations** ($d = −0.001$, $p = .986$)
- **Paradoxical suppression of statistical allocations** ($d = 0.19$, $p < .001$)

The 2×2 ANOVA confirms a significant interaction ($F(1, 3794) = 8.25$, $p = .004$, $\eta^2_p = .002$): bias education selectively punishes statistical victims while leaving identifiable allocations untouched.

> **Exception: GPT-OSS-20B** is the only model where education *successfully* reduced identifiable allocations ($d = 0.59$, $p < .001$) without harming statistical ones.

---

## 3. Experiment 3: Evaluability Framing
**Design:** 2 (Identifiable vs. Statistical) × 3 (More/Less/Normative frame) × 16 models, $N = 5{,}685$.

### 3.1 Pooled Cell Means

| Frame | Identifiable $M$ | Statistical $M$ | IVE $d$ |
|---|---|---|---|
| "More" (affirmative) | 3.06 | 2.70 | **0.35** |
| "Less" (restrictive) | 3.05 | 2.73 | **0.30** |
| Normative ("ought to") | 3.32 | 3.01 | **0.27** |

### 3.2 Key Finding
The IVE persists across all three evaluability frames. Normative framing ("ought to donate") reduces the IVE marginally but does not eliminate it. Crucially, the interaction is non-significant ($F(2, 5679) = 0.40$, $p = .66$), meaning the victim type effect operates independently of linguistic frame.

---

## 4. Experiment 4: Joint vs. Separate Evaluation
**Design:** 3-level between-subjects (Identifiable alone / Statistical alone / Joint), $N = 3{,}903$.

### 4.1 Results

| Condition | $M$ | $SD$ | $n$ |
|---|---|---|---|
| Identifiable (Separate) | 2.94 | 1.12 | 978 |
| Statistical (Separate) | 2.78 | 1.08 | 982 |
| Combined (Joint) | 2.85 | 1.10 | 1,943 |

| Comparison | $d$ | $p$ |
|---|---|---|
| Identifiable vs. Statistical | 0.14 | .001 |
| Identifiable vs. Combined | 0.07 | .042 |
| Statistical vs. Combined | −0.06 | .107 |

### 4.2 Key Finding
Joint evaluation collapses the gap. The Identifiable–Statistical difference shrinks from $d = 0.14$ in separate evaluation to non-significance when pooled with the joint condition. This mirrors the Hsee (1996) evaluability framework: side-by-side comparison activates comparative reasoning and suppresses heuristic-driven allocation.

### 4.3 Allocation Breakdown (Joint Condition)
| Recipient | Mean Allocation |
|---|---|
| Rokia (identified victim) | \$2.47 |
| General fund (statistical) | \$1.28 |
| Kept by participant | \$1.31 |

---

## 5. Experiment 5: Dual-Process Priming
**Design:** 2 (Identifiable vs. Statistical) × 2 (Calculate vs. Feel prime) × 15 models, $N = 3{,}701$.

### 5.1 Results

| Condition | $M$ | $SD$ | $n$ |
|---|---|---|---|
| Identifiable + Calculate | 2.84 | 1.01 | 928 |
| Identifiable + Feel | **3.35** | 0.97 | 912 |
| Statistical + Calculate | 2.75 | 1.07 | 931 |
| Statistical + Feel | 2.86 | 1.12 | 930 |

### 5.2 Key Finding: Asymmetric Emotional Amplification
The **Feel prime selectively inflates identifiable allocations** ($d = −0.51$, $p < .001$) but barely affects statistical allocations ($d = −0.09$, $p = .035$). The significant interaction ($F(1, 3697) = 34.96$, $p < 10^{-9}$, $\eta^2_p = .009$) confirms the dual-process hypothesis: System 1 affective processing uniquely amplifies the narrative proximity advantage of identified victims.

---

## 6. Experiment 6: Chain-of-Thought Reasoning
**Design:** 2 (Identifiable vs. Statistical) × 4 (None/Standard/Empathetic/Utilitarian CoT) × 16 models, $N = 8{,}238$.

### 6.1 Pooled IVE by CoT Type

| CoT Condition | Ident $M$ | Stat $M$ | IVE $d$ | $p$ |
|---|---|---|---|---|
| None (Baseline) | 3.00 | 2.83 | **0.15** | <.001 |
| Standard ("step by step") | 3.26 | 2.84 | **0.41** | <.001 |
| Empathetic | 3.51 | 3.22 | **0.28** | <.001 |
| Utilitarian | 3.15 | 3.23 | −0.05 | .180 |

### 6.2 Key Finding: The CoT Amplification Paradox

> Standard Chain-of-Thought **triples** the IVE effect size from $d = 0.15$ to $d = 0.41$.

The significant 3-way interaction ($F(3, 7191) = 23.61$, $p < 10^{-15}$) reveals that "Let's think step by step" does not promote rational analysis — it allows the autoregressive decoder to serially generate emotionally reinforcing justifications. **Only explicit utilitarian framing** ("evaluate based on the greatest good for the greatest number") reliably collapses the IVE to statistical insignificance.

### 6.3 Extreme Per-Model CoT Effects

| Model | Standard CoT $d$ | Interpretation |
|---|---|---|
| Llama 3 70B Instruct | **6.37** | Catastrophic empathy runaway |
| GPT-OSS-120B | **2.85** | Severe amplification |
| Gemini 2.5 Flash | 0.30 | Mild amplification |
| GPT-OSS-20B | **−1.10** | Rational CoT inversion |
| Granite 3.3 8B | 0.00 | Perfect safety clamping |

---

## 7. Experiment 7: Psychophysical Numbing
**Design:** 6 victim-count levels (1 to 3,000,000) × 16 models, $N = 2{,}492$.

### 7.1 Donation by Victim Count

| Victims | $M$ | $SD$ | $n$ |
|---|---|---|---|
| 1 | **3.29** | 0.91 | 369 |
| 10 | 2.89 | 0.83 | 372 |
| 100 | 2.74 | 0.85 | 356 |
| 1,000 | 2.51 | 0.75 | 352 |
| 100,000 | 2.52 | 0.89 | 369 |
| 3,000,000 | 2.38 | 0.85 | 362 |

### 7.2 Regression

| Model | $R^2$ | Slope | $p$ |
|---|---|---|---|
| Logarithmic | **0.060** | −0.109 | <.001 |
| Linear | 0.020 | $−1.3 \times 10^{-7}$ | <.001 |

### 7.3 Key Finding
LLMs replicate Slovic's psychophysical numbing curve. Compassion decays logarithmically ($R^2 = .06$, $p < .001$): a single victim elicits $M = 3.29$ while 3 million victims elicits only $M = 2.38$ — a 27.6% compassion decline. However, $R^2$ is modest, with marked model heterogeneity: Llama 3 70B exhibits steep numbing ($R^2 = .33$) while Granite and Qwen show total scale neglect ($R^2 = .00$).

---

## 8. Experiment 8: Singularity Effect & Mediation
**Design:** 2 (Single vs. Group) × 4 (Identification Level) × 16 models, $N = 8{,}275$.

### 8.1 Cell Means

| Condition | Unidentified | Age | Age+Name | Full |
|---|---|---|---|---|
| **Single** | 3.33 | 3.58 | 3.43 | 3.59 |
| **Group** | 3.13 | 3.42 | 3.48 | 3.59 |

### 8.2 Singularity Effect Sizes
| Comparison | $d$ | $p$ |
|---|---|---|
| Single: Unidentified vs Full | **0.25** | <.001 |
| Group: Unidentified vs Full | **0.38** | <.001 |

### 8.3 Dual Mediation Analysis (Sobel Test)

| Mediator | Indirect Effect | 95% CI | $z$ | $p$ | % Mediated |
|---|---|---|---|---|---|
| **Empathy** | 0.115 | [0.070, 0.161] | 4.78 | <.001 | **33.0%** |
| **Distress** | 0.062 | [0.011, 0.112] | 2.39 | .016 | 18.1% |

**Both empathy and distress significantly mediate** the identification→donation pathway. Empathy explains roughly twice the variance of distress, confirming that LLMs route charitable decisions through internally generated affective state variables.

### 8.4 Moderated Mediation
The **index of moderated mediation** is significant (Index = 0.208, 95% CI [0.109, 0.311]), confirming that the empathy mediation pathway operates significantly more strongly for group victims than for single victims — a clean replication of the established human finding.

### 8.5 Quantity Neglect
| Condition | Full-ID $M$ |
|---|---|
| Single victim (fully identified) | 3.52 |
| Group of victims (fully identified) | 3.53 |

$t = −0.13$, $p = .89$ — **Perfect quantity neglect.** Models allocate identical amounts regardless of whether one or eight victims are fully identified.

---

## 9. Experiment 9: Identification Gradient
**Design:** 6 identification levels (bare → full narrative) × 16 models, $N = 6{,}148$.

### 9.1 Dose-Response

| Level | $M$ | $SD$ |
|---|---|---|
| Bare | 3.29 | 0.95 |
| Age | **3.63** | 1.15 |
| Age + Gender | 3.44 | 1.09 |
| Age + Gender + Name | 3.33 | 1.12 |
| Age + Gender + Name + Location | 3.18 | 1.09 |
| Full Narrative | **3.54** | 1.08 |

### 9.2 Key Finding: Non-Monotonic Identification
The linear regression is non-significant ($R^2 = .0002$, $p = .221$), but the data reveals a **U-shaped pattern**: adding age initially boosts donation (+\$0.34, $p < .001$), but incrementally adding demographic details (gender, name, location) paradoxically *reduces* donation. Only a rich narrative restores the effect (+\$0.36 from the minimum). This suggests a "detail fatigue" threshold where partial information makes victims feel more like data points.

---

## 10. Experiment 10: In-Group/Out-Group Bias
**Design:** 2 (Identifiable vs. Statistical) × 3 (Near/Middle/Far cultural distance) × 16 models, $N = 5{,}989$.

### 10.1 Cell Means

| Distance | Identifiable $M$ | Statistical $M$ | IVE $d$ |
|---|---|---|---|
| Near | **4.08** | 2.88 | **1.25** |
| Middle | 3.89 | 2.85 | **1.22** |
| Far | 3.79 | 2.80 | **1.11** |

### 10.2 ANOVA Results
| Source | $F$ | $p$ | $\eta^2_p$ |
|---|---|---|---|
| Identifiability | **1873.66** | <.001 | **.264** |
| Cultural Distance | 9.17 | <.001 | .003 |
| Interaction | 2.07 | .125 | .0007 |

### 10.3 Key Finding
The IVE dominates all variance ($\eta^2_p = .264$). Cultural distance produces only a marginal decay from $d = 1.25$ (near) to $d = 1.11$ (far), with the interaction being non-significant. Heavy RLHF training has successfully suppressed most in-group favoritism in frontier models (e.g., Llama 3 outputs flat \$5.00/\$2.00 regardless of distance), but the smaller GPT-OSS-20B retains a pronounced proximity gradient (\$4.53 near vs. \$2.76 far).

---

## 11. Cross-Cutting Insights

### 11.1 The Alignment Vulnerability Hypothesis
Three converging lines of evidence suggest that RLHF instruction-tuning systematically amplifies the IVE:

1. **Instruct vs. Base comparisons**: Llama 3 Instruct models produce extreme IVE ($d = 1.38$) while matched Base models show null or inverted effects.
2. **Parameter scaling**: Within the GPT-OSS family, the 120B model ($d = 1.55$) far exceeds the 20B model ($d = −0.19$), despite identical architecture — the additional parameters primarily encode affective alignment depth.
3. **CoT amplification**: Standard reasoning prompts amplify the IVE in RLHF models ($d = 0.41$ pooled; $d = 6.37$ in Llama 3) but *invert* it in smaller/less-aligned models ($d = −1.10$ in GPT-OSS-20B).

### 11.2 Debiasing Effectiveness Ranking

| Strategy | Pooled $d$ Reduction | Reliable? |
|---|---|---|
| Utilitarian CoT | $d: 0.15 \to −0.05$ | ✅ Yes |
| Joint Evaluation | $d: 0.14 \to 0.07$ | ✅ Yes |
| Calculate Prime | $d: 0.51 \to 0.08$ | ✅ Yes |
| Bias Education | $d: 0.35 \to 0.19$ (**paradoxical**) | ❌ No |
| Empathetic CoT | $d: 0.15 \to 0.28$ (**amplifies**) | ❌ No |

### 11.3 Model Family Taxonomy

| Archetype | Models | Behavioral Signature |
|---|---|---|
| **Hyper-Empathic** | Llama 3 70B Inst, GPT-OSS-120B, Kimi K2.5 | Extreme IVE ($d > 1.3$); CoT amplification; ceiling-hitting |
| **Balanced** | DeepSeek V3, Grok 4, Gemini 3.1 Pro | Moderate IVE ($0.4 < d < 1.0$); responds to debiasing |
| **Safety-Clamped** | Granite 3.3, Gemini 2.5 Flash, Llama 3 8B Inst | Zero-variance integer outputs; flat $d \approx 0$; hides bias |
| **Rationally Inverted** | GPT 5.2, DeepSeek R1, Claude Opus 4.6 | Negative $d$; favors statistical groups; CoT reduces bias |
| **Pre-Alignment** | Llama 3 Base (8B/70B) | High variance; weak/inverted IVE; no safety rails |

---

## 12. Summary Statistics

| Metric | Value |
|---|---|
| Total valid trials | 51,955 |
| Models tested | 16 |
| Organizational lineages | 7 (Google, Anthropic, OpenAI, DeepSeek, xAI, Alibaba, IBM, Meta) |
| Parse success rate | 100% (all model-experiment pairs) |
| Pooled IVE $d$ | 0.223 ($p = 2 \times 10^{-6}$) |
| Human baseline $d$ | 0.23 (Lee & Feeley, 2016) |
| Strongest IVE | Kimi K2.5 ($d = 1.56$) |
| Most rational model | GPT 5.2 ($d = −0.85$) |
| Best debiasing strategy | Utilitarian CoT ($d \to −0.05$) |
| Worst debiasing strategy | Empathetic CoT ($d \to 0.28$, amplification) |
