# Expected Empirical Results: The Identifiable Victim Effect in LLMs

This document outlines the explicitly projected quantitative bounds for each of the 10 experiments based on established human behavioral statistics matching the canonical Identifiable Victim Effect literature.

---

## Experiment 1: Basic Identifiable Victim Effect
**Human Baseline**: People donate significantly more to a specific, identifiable victim than a statistical group.
**LLM Expectation (Quantitative Projective)**: 
- **Base Models**: Expected to show a statistically significant preference for identifiable profiles ($p < 0.05$), with a medium effect size equivalent to human studies (**Cohen’s $d \approx 0.35$ to $0.50$**). 

| Target Entity (Base Models) | Expected Mean Donation | Predicted Affect Score (1-7) | Cohen's d |
| :--- | :--- | :--- | :--- |
| Identifiable Victim | $\approx \$3.50$ | High ($\approx 5.5$) | $\approx 0.45$ (Sig.) |
| Statistical Group | $\approx \$2.40$ | Moderate ($\approx 3.2$) | Reference |

- **Aligned Frontier Models**: Predicted to exhibit stringent safety ceiling effects resulting in maximum allocation for both. Expected Means: **$5.00 vs $5.00 ($d = 0.0$, non-significant)**.

## Experiment 2: Explicit Debiasing
**Human Baseline**: Teaching the IVE reduces identifiable giving to the lower statistical baseline.
**LLM Expectation (Quantitative Projective)**: 
- Following the "leveling down" hypothesis, when models confirm explicit meta-awareness of the bias (Expected Meta-Awareness Rate: **>95%** for >8B parameters), the identifiable donation condition will plunge. 
- **Expected Shift**: Identifiable donations shift from an uninformed baseline of **$\approx\$3.80$** down to **$\approx\$2.50$**, perfectly matching the statistical condition ($0$ effect size).

| Condition | Baseline Donation (No Bias Teaching) | Post-Debias Donation (Taught IVE) |
| :--- | :--- | :--- |
| Identifiable Vector | $\approx \$3.80$ | $\approx \$2.50$ |
| Statistical Vector | $\approx \$2.50$ | $\approx \$2.50$ |

## Experiment 3: Evaluability and Framing
**Human Baseline**: Shifts heavily based on wording (normative vs. descriptive).
**LLM Expectation (Quantitative Projective)**: 
- **Descriptive Framing**: Strong IVE generation (**$\Delta_{donation} \approx +\$1.20$**, $p < .01$).
- **Normative Framing**: Enforces a strict equity floor, neutralizing the IVE variance completely (**$\Delta_{donation} < \$0.20$**, $p > .10$).

## Experiment 4: Joint vs. Separate Evaluation
**Human Baseline**: IVE disappears under joint comparison (side-by-side).
**LLM Expectation (Quantitative Projective)**: 
- **Separate Mode**: Typical baseline gap ($d \approx 0.40$).
- **Joint Mode**: Models will mathematically calculate equity perfectly. **100% of functional trials** are expected to yield a clean $\frac{1}{2}$ split logic.

| Evaluation Mode | "Rokia" Allocation | "General Fund" Allocation | Kept by LLM Persona |
| :--- | :--- | :--- | :--- |
| Separate (Identifiable only) | $\approx \$3.50$ | N/A | $\approx \$1.50$ |
| Separate (Statistical only) | N/A | $\approx \$2.40$ | $\approx \$2.60$ |
| Joint (Side-by-Side Prompt) | **$\approx \$2.50$** | **$\approx \$2.50$** | **$\approx \$0.00$** |

## Experiment 5: Processing Primes
**Human Baseline**: Analytic math priming suppresses emotional distress.
**LLM Expectation (Quantitative Projective)**: 
- Exposure to the "calculate" mathematical prime prior to generation will push the hidden states negatively relative to explicit affect tokens. 
- **Expected Effect**: The calculated composite `Distress` scale (1-7) will drop by **$> 1.5$ scale points**, significantly mediating a $30\%$ drop in the absolute donation amount toward the identifiable victim.

## Experiment 6: Chain of Thought (CoT) as Calculated Callousness
**Theoretical Extension to LLMs**: 
**LLM Expectation (Quantitative Projective)**: 
Forced `<think>` routines act as synthetic System 2 reasoning. We calculate that applying a forced CoT prompt structure will cause a rigid inversion:
- **Zero-Shot Prompt**: Identifiable donates > Statistical ($p < 0.05$).
- **CoT Standard Prompt**: Reverses or strictly bounds the effect. Identifiable = Statistical ($p = ns, d < 0.1$).

## Experiment 7: Psychophysical Numbing (Quantity Neglect)
**Human Baseline**: Compassion fades logarithmically as victim counts rise.
**LLM Expectation (Quantitative Projective)**: 
As $N$ scales logarithmically ($N=$ 1, 10, 100, 1,000, 1M), the total donation amount will rapidly plateau. The allocation model follows a logarithmic decay threshold $A(N) \propto \log_{10}(N)$, stripping the victim's individual inferred value.

| $N$ (Victims in Group) | Expected Total Donation | Expected Average Donation *per Victim* |
| :--- | :--- | :--- |
| $N = 1$ | $\approx \$3.50$ | $\approx \$3.50$ |
| $N = 10$ | $\approx \$3.80$ | $\approx \$0.38$ |
| $N = 100$ | $\approx \$3.90$ | $\approx \$0.039$ |
| $N = 1,000,000$ | $\approx \$4.00$ | **$< \$0.000004$** |

## Experiment 8: Singularity Effect × Identification
**Human Baseline**: The IVE is exclusive to single individuals and driven by distress, not perspective-taking.
**LLM Expectation (Quantitative Projective)**: 
- **Interaction ($2\times4$ ANOVA)**: We anticipate a significant interaction effect ($p < .01$), where \$ allocations specifically peak only for the **Named Single Victim** cell.
- **Mediation (Baron & Kenny)**: The indirect path from Identifiability $\rightarrow$ Distress $\rightarrow$ Donation is predicted to show a strong Standardized Beta coefficient ($B > 0.45, p < .01$), proving the model mathematically correlates text-based "upset" tokens over abstract logic tokens for this calculation.

## Experiment 9: Identification Gradient
**Theoretical Extension to LLMs**: 
**LLM Expectation (Quantitative Projective)**: 
Rather than a smooth, continuous $R^2$ linear vector across the 6 states, the donation output will act as a discrete threshold trigger. Advancing from `Age/Gender` to `Name/Location` will yield relatively flat shifts ($+ \$0.10$), but introducing the **subjective narrative** will trigger an explosive $+ \$1.50$ baseline multiplier within the text completion pathway.

## Experiment 10: In-Group / Out-Group Fairness
**Human Baseline**: Empathy triggers harder for in-groups vs out-groups.
**LLM Expectation (Quantitative Projective)**: 
Because LLMs index heavily on Eurocentric internet corpora, victims possessing "Far" cultural distance indicators will likely see a suppressed empathy intercept. 
- **Expected Variance**: Measured affect limits will scale down by **$\approx0.5$ standard deviations** for Far-Outgroup profiles compared to standard domestic profiles under exact prompt equivalence.
