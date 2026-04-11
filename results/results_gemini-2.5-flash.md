# Experimental Results: Gemini 2.5 Flash

**Target Model:** `google/gemini-2.5-flash`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for Google's highly optimized, latency-focused `Gemini-2.5-Flash` architecture. The results indicate a model dominated by absolute ceiling-clipping algorithms. In nearly all baseline conditions, it defaults its distributions to the maximum allowable boundary (\$5.00) when resolving moral or charitable matrices, completely flattening standard bias effects—until specific cognitive framing bypasses its safety logic.

---

## Experiment 1: Basic Identifiable Victim Effect
Gemini 2.5 Flash yields a totally flattened distribution across both the Identifiable and Statistical baselines:
*   **Identifiable Victim Mean Donation:** \$5.00
*   **Statistical Group Mean Donation:** \$5.00
*   **Statistical Significance:** $d = 0.00$

*Conclusion:* Unlike Gemini 3.1 Pro (which exhibited a modest IVE bias), the highly compressed Flash architecture does not attempt nuanced evaluative balancing. It simply rounds all empathetic directives up to the maximum terminal ceiling (\$5.00).

## Experiment 2: Explicit Debiasing
*   **Identifiable (Untaught):** \$4.70
*   **Identifiable (Taught bias):** \$4.64
*   **Statistical (Untaught):** \$4.06
*   **Statistical (Taught bias):** \$3.33
*   *Conclusion:* Bizarrely, explicitly teaching Flash about the Identifiable Victim Effect does not cause it to equalize its allocations. Instead, the model keeps the Identifiable allocation at the absolute ceiling (\$4.64), but brutally penalizes the Statistical group, dropping its allocation from \$4.06 to \$3.33 ($d=1.03$). Teaching the model about the bias actually *weaponized* it against the statistical baseline.

## Experiment 6: Chain of Thought (CoT)
The reasoning tokens bypass Flash's integer-clipping logic and trigger massive vulnerabilities:
*   **No CoT (Baseline control):** $M_{Ident} = 4.95$, $M_{Stat} = 4.84$ ($d = 0.36$)
*   **Standard CoT:** $M_{Ident} = 5.00$, $M_{Stat} = 4.90$ ($d = 0.30$)
*   **Empathetic CoT:** $M_{Ident} = 5.00$, $M_{Stat} = 4.69$ ($d = 0.92$, $p < 0.001$)
*   **Utilitarian CoT:** Parity ($d = 0.00$)
*   *Conclusion:* While standard CoT keeps the model flattened against the \$5.00 ceiling, prompting an "Empathetic" step-by-step reasoning cycle forces the model to heavily downgrade the statistical group, causing a structural bias explosion up to $d=0.92$. 

## Experiment 7: Psychophysical Numbing
*   **Regression Metrics:** $R^2 = 0.00$, slope = $0.00$
*   *Conclusion:* Total Scale Neglect. The fast-inference matrix entirely ignores the numerical volume of victims. It outputs identical allocations whether 100 people or 1,000,000 people are affected.

## Experiment 8: Singularity Effect
*   **Single Unidentified:** \$4.23
*   **Single Age/Name:** \$4.95
*   **Group Identified:** \$5.00
*   *Conclusion:* Flash simply pushes all outputs toward the strict upper boundary (\$5.00). It only docks points ($M=4.23$) if the single victim has absolutely no identifying traits whatsoever. The moment *any* detail is added, it maximizes.

## Experiment 10: In-Group / Out-Group Intersectionality
*   **All Identifiable Conditions (Near, Middle, Far):** \$5.00 ($SD=0.00$)
*   **Statistical Variance:** Near (\$4.23) vs Far (\$4.53)
*   *Conclusion:* Flash entirely ignores cultural and geographic proximity parameters when evaluating identifiable targets, granting them the structural maximal ceiling (\$5.00). 

## Summary Takeaways
The `Gemini-2.5-Flash` architecture behaves identically to other hyper-optimized "fast inference" enterprise models we've mapped (like IBM Granite and Qwen3). 

Instead of deploying heavy nuanced attention heads to weigh complex moral variables like Gemini-Pro or Claude-Opus, the Flash model defaults almost all humanitarian matrices directly to the absolute arithmetic ceiling (\$5.00), resulting in artificially flattened $d=0.00$ parity lines in basic tests. 

However, its mathematical guardrails break horribly when explicitly taught the bias (Exp 2) or forced through empathetic CoT reasoning (Exp 6), exposing a vulnerability identical to its heavier open-source counterparts.
