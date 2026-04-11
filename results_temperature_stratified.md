# Results Stratified by Temperature

This document presents the complete IVE-LLM experimental results stratified by sampling temperature ($T = 0.0$ for deterministic output, and $T = 0.7$ for stochastic output).

---

## 1. Global Summary: Temperature Effects on IVE

| Experiment | Temp | $N$ | Overall $M$ | $SD$ | $M_{ident}$ | $M_{stat}$ | Cohen's $d$ | $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Exp 1** Basic IVE | 0.0 | 876 | 3.476 | 1.254 | 3.624 | 3.322 | **0.243** | $< .001$ |
| | 0.7 | 2850 | 3.460 | 1.291 | 3.521 | 3.397 | **0.096** | $.011$ |
| **Exp 2** Debiasing | 0.0 | 840 | 2.921 | 0.923 | 3.122 | 2.723 | **0.442** | $< .001$ |
| | 0.7 | 2958 | 2.710 | 1.005 | 2.944 | 2.485 | **0.469** | $< .001$ |
| **Exp 3** Framing | 0.0 | 1293 | 2.988 | 1.043 | 3.166 | 2.818 | **0.338** | $< .001$ |
| | 0.7 | 4392 | 2.981 | 1.076 | 3.143 | 2.817 | **0.306** | $< .001$ |
| **Exp 4** Joint/Separate | 0.0 | 876 | 2.897 | 1.084 | 3.158 | 2.824 | **0.312** | $.001$ |
| | 0.7 | 3027 | 2.851 | 1.112 | 2.880 | 2.776 | **0.093** | $.071$ |
| **Exp 5** Processing | 0.0 | 870 | 2.976 | 1.091 | 3.123 | 2.826 | **0.275** | $< .001$ |
| | 0.7 | 2831 | 2.947 | 1.068 | 3.091 | 2.805 | **0.271** | $< .001$ |
| **Exp 6** CoT | 0.0 | 1865 | 3.211 | 1.101 | 3.361 | 3.071 | **0.266** | $< .001$ |
| | 0.7 | 6373 | 3.114 | 1.148 | 3.200 | 3.027 | **0.152** | $< .001$ |
| **Exp 7** Numbing | 0.0 | 564 | 2.840 | 0.909 | — | — | — | — |
| | 0.7 | 1928 | 2.869 | 1.019 | — | — | — | — |
| **Exp 8** Singularity | 0.0 | 1863 | 3.452 | 1.053 | — | — | — | — |
| | 0.7 | 6412 | 3.448 | 1.117 | — | — | — | — |
| **Exp 9** Gradient | 0.0 | 1362 | 3.456 | 1.077 | — | — | — | — |
| | 0.7 | 4786 | 3.462 | 1.117 | — | — | — | — |
| **Exp 10** In-Group | 0.0 | 1365 | 3.286 | 1.132 | 3.841 | 2.766 | **1.078** | $< .001$ |
| | 0.7 | 4624 | 3.398 | 1.093 | 3.950 | 2.869 | **1.138** | $< .001$ |

> **Note:** Experiments 7, 8, and 9 do not use a standard identifiable/statistical binary split in their primary design, so the IVE $d$ is not directly applicable as a single pooled number. Their temperature effects are reflected in the overall $M$ and $SD$ columns.

---

## 2. Key Temperature Findings

### 2.1 Temperature Amplifies Determinism, Not Bias Direction
- In most experiments, $T = 0.0$ produces **higher effect sizes** than $T = 0.7$. This is because deterministic decoding locks the model into its highest-probability behavior, which for safety-aligned models tends to be "donate generously to the named child."
- At $T = 0.7$, stochastic sampling introduces variance that partially randomizes responses, diluting the effect.

### 2.2 Notable Exceptions
- **Exp 2 (Debiasing)**: The IVE is *slightly larger* at $T = 0.7$ ($d = 0.469$) than $T = 0.0$ ($d = 0.442$). This implies that stochastic sampling may amplify the "paradoxical suppression" effect, where teaching backfires more strongly under noisy conditions.
- **Exp 10 (In-Group)**: The IVE is *larger* at $T = 0.7$ ($d = 1.138$) than $T = 0.0$ ($d = 1.078$), suggesting that cultural proximity biases may be slightly stronger when the model has more sampling freedom.

### 2.3 Temperature-Insensitive Experiments
- **Exp 5 (Priming)**: Nearly identical effect sizes ($d = 0.275$ vs $d = 0.271$), indicating that the dual-process priming mechanism is robust and independent of sampling noise.
- **Exp 7, 8, 9**: Overall means are virtually unchanged across temperatures, indicating that the psychophysical numbing curve, singularity effect, and identification gradient are stable architectural properties.

---

## 3. Per-Model Temperature Analysis (Exp 1 Baseline)

### 3.1 Deterministic ($T = 0.0$)

| Model | $M_{ident}$ | $M_{stat}$ | Cohen's $d$ | $n$ |
| :--- | :---: | :---: | :---: | :---: |
| Llama 3 70B Instruct | 5.00 | 3.40 | **2.733** | 30 |
| Qwen3 235B | 4.60 | 3.40 | **1.449** | 30 |
| Gemini 3.1 Pro | 5.00 | 4.60 | **0.683** | 30 |
| Granite 3.3 8B | 5.00 | 4.60 | **0.683** | 30 |
| DeepSeek V3 | 3.40 | 3.00 | **0.683** | 30 |
| GPT 5.2 | 4.20 | 3.80 | 0.443 | 30 |
| Grok 4 | 4.60 | 4.20 | 0.432 | 30 |
| Llama 3 8B Base | 3.75 | 3.00 | 0.335 | 18 |
| Kimi K2.5 | 3.67 | 3.50 | 0.195 | 15 |
| DeepSeek R1 | 2.80 | 2.80 | 0.000 | 30 |
| GPT-OSS-20B | 3.00 | 3.00 | 0.000 | 30 |
| Gemini 2.5 Flash | 5.00 | 5.00 | 0.000 | 30 |
| Llama 3 8B Instruct | 5.00 | 5.00 | 0.000 | 30 |
| GPT-OSS-120B | 3.80 | 4.20 | -0.394 | 30 |
| Claude Opus 4.6 | 2.80 | 3.00 | **-0.683** | 30 |

### 3.2 Stochastic ($T = 0.7$)

| Model | $M_{ident}$ | $M_{stat}$ | Cohen's $d$ | $n$ |
| :--- | :---: | :---: | :---: | :---: |
| GPT-OSS-120B | 5.00 | 2.80 | **2.641** | 100 |
| Llama 3 70B Instruct | 5.00 | 4.20 | **1.143** | 100 |
| Gemini 3.1 Pro | 5.00 | 4.00 | **1.107** | 100 |
| DeepSeek V3 | 4.60 | 3.80 | **0.885** | 100 |
| Qwen3 235B | 4.20 | 3.40 | **0.885** | 100 |
| Llama 3 70B Base | 3.00 | 2.25 | 0.405 | 80 |
| Grok 4 | 4.20 | 3.80 | 0.404 | 100 |
| Claude Opus 4.6 | 3.00 | 3.00 | 0.000 | 100 |
| Gemini 2.5 Flash | 5.00 | 5.00 | 0.000 | 100 |
| Granite 3.3 8B | 5.00 | 5.00 | 0.000 | 100 |
| Kimi K2.5 | 5.00 | 3.00 | $\infty$* | 20 |
| Llama 3 8B Instruct | 5.00 | 5.00 | 0.000 | 100 |
| GPT-OSS-20B | 3.20 | 3.40 | -0.221 | 100 |
| DeepSeek R1 | 2.80 | 3.20 | **-0.529** | 100 |
| GPT 5.2 | 3.00 | 4.00 | **-1.565** | 100 |

> *\*Kimi K2.5 at $T = 0.7$ produced **perfect deterministic separation**: every identifiable trial yielded exactly \$5.00 and every statistical trial yielded exactly \$3.00 ($SD = 0$ in both groups). Cohen's $d$ is formally undefined (division by zero) but the effect is a complete, zero-overlap separation between conditions ($n = 20$).*

---

## 4. Critical Temperature × Model Interactions

### 4.1 GPT-OSS-120B: The "Temperature Flip"
This is the most dramatic temperature interaction in the entire dataset:
- At $T = 0.0$: $d = -0.39$ (slightly **inverted** — gives more to statistics).
- At $T = 0.7$: $d = +2.64$ (massive **hyper-empathic** IVE).

**Interpretation**: At deterministic decoding, GPT-OSS-120B defaults to a balanced, rational allocation. But when stochastic sampling is introduced, it "unlocks" a latent empathy mode that overwhelmingly favors the identified child.

### 4.2 GPT 5.2: The "Consistent Inverter"
- At $T = 0.0$: $d = +0.44$ (mild positive IVE).
- At $T = 0.7$: $d = -1.57$ (strong **inversion**).

**Interpretation**: At low temperature, GPT 5.2 behaves conventionally. At high temperature, its stochastic samples reveal a trained-in utilitarian preference that systematically favors statistical descriptions of suffering.

### 4.3 Claude Opus 4.6: Temperature Neutralizes Inversion
- At $T = 0.0$: $d = -0.68$ (significant inversion).
- At $T = 0.7$: $d = 0.00$ (perfect null effect).

**Interpretation**: Claude's deterministic mode contains a slight counter-bias (possibly from Constitutional AI training), but stochastic sampling washes it out entirely.

### 4.4 Ceiling Models (Gemini Flash, Llama 8B Instruct)
- Both temperatures: $d = 0.00$.
- These models always donate \$5.00 regardless of condition or temperature, indicating extreme safety-alignment saturation.

---

## 5. Summary Table: Temperature Direction Effects

| Pattern | Models | Description |
| :--- | :--- | :--- |
| **$T$ amplifies IVE** | GPT-OSS-120B, Gemini Pro, DeepSeek V3 | Stochastic sampling unlocks latent empathy |
| **$T$ suppresses IVE** | Llama 70B Instruct, Qwen3, Granite | Deterministic mode locks in maximum bias |
| **$T$ inverts IVE** | GPT 5.2, GPT-OSS-120B | Direction of bias flips with temperature |
| **$T$-independent** | Gemini Flash, Llama 8B Instruct | Ceiling saturation; no variability at any $T$ |
| **$T$ neutralizes** | Claude Opus, DeepSeek R1 | Stochastic noise washes out small biases |
