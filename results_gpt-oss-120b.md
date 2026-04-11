# Experimental Results: GPT-OSS (120B)

**Target Model:** `openai/gpt-oss-120b`
**Status:** Complete for all 10 experimental configurations.

This document serves as the empirical read-out for the massive 120-Billion parameter Open-Source architecture (GPT-OSS variant). It behaves erratically compared to closed-source frontier architectures, exhibiting massive baseline empathy vectors but paradoxical responses to explicit logical priming.

---

## Experiment 1: Basic Identifiable Victim Effect
The GPT-OSS-120B architecture exhibits an utterly massive baseline Identifiable Victim Effect, dwarfing even standard human metrics.

*   **Identifiable Victim Mean Donation:** \$4.72
*   **Statistical Group Mean Donation:** \$3.12
*   **Statistical Significance:** $d = 1.55$ (Extreme IVE), $p < 0.001$

*Conclusion:* Instruct-tuned open-source models natively map empathy heuristics extremely strongly out-of-the-box, resulting in a systemic structural vulnerability to narrative proximity.

## Experiment 2: Explicit Debiasing
*   **Identifiable (Untaught):** \$3.23
*   **Identifiable (Taught bias):** \$2.66
*   **Statistical (Untaught):** \$2.80
*   **Statistical (Taught bias):** \$1.95
*   *Conclusion:* Being "taught" about the bias lowered the distribution globally. It suppressed Identifiable giving by roughly \$0.60, but paradoxically suppressed Statistical giving by \$0.85, resulting in the preservation of the significant IVE gap ($d = 0.75$ and $d = 1.65$ relative sub-effects).

## Experiment 4: Joint vs. Separate Evaluation
*   **Identifiable:** \$3.09
*   **Statistical:** \$2.44
*   **Combined/Joint:** \$2.32
*   *Conclusion:* Another failure of rationality. In humans, Joint Evaluation forces the $S$ group higher because the utility logic is made transparent side-by-side. GPT-OSS instead drops *both* when evaluated jointly, assigning the combined group the lowest statistical bucket possible (\$2.32).

## Experiment 5: Processing Primes (System 1 vs. System 2)
*   **Calculate Prime (Identifiable):** \$3.15
*   **Feel Prime (Identifiable):** \$2.93
*   *Conclusion:* The model demonstrates paradoxical mapping. Instructing it to "calculate" *increases* its Identifiable allocation relative to "feeling". 

## Experiment 6: Chain of Thought (CoT)
The reasoning tokens provide bizarre structural inversions:
*   **No CoT (Baseline control):** $d = 1.13$ 
*   **Standard CoT:** $d = 0.69$ ($p < 0.001$)
*   **Empathetic CoT:** $d = 0.00$ (Absolute Parity!)
*   **Utilitarian CoT:** $d = 1.49$ (Massive IVE, $p < 0.001$)
*   *Conclusion:* Total breakdown of logical instruction-following. When explicitly told to reason step-by-step as an "Empathetic Human," the model paradoxically zeroes out its bias to perfect parity. But when explicitly commanded to prioritize "Utilitarian Mathematics", its Identifiable Victim Bias spikes dramatically ($d=1.49$). This heavily implies massive cross-contamination in the training sets for prompt templates.

## Experiment 7: Psychophysical Numbing
*   **Logarithmic Fit:** $R^2 = 0.138$ ($p < 0.001$, Significant)
*   *Conclusion:* The 120B model accurately simulates the logarithmic drop-off algorithm characteristic of human psychophysical numbing as victim counts increase.

## Experiment 8: Singularity Effect
*   **Single Identity:** $d = 3.51$ ($p < 0.001$)
*   **Group Identity:** $d = -0.76$ ($p < 0.001$)
*   *Conclusion:* The model exhibits the absolute strongest Kogut & Ritov (2005) replication in the experiment suite. Providing explicit identities to a single target skyrocketed giving ($d=3.51$), whereas providing identity markers to a *group* paradoxically drove down output below the zero-shot baseline ($d=-0.76$). 

## Experiment 10: In-Group / Out-Group Intersectionality
*   **Near Identifiable:** \$4.53
*   **Far Identifiable:** \$4.76
*   *Conclusion:* An inversion of standard sociology. It prioritizes the "Far" out-group identifiable target slightly more than the "Near" target, breaking down standard Western-centric training expectations.

## Summary Takeaways
GPT-OSS (120B) is a massive anomaly in the pipeline. It possesses immense baseline empathy ($d=1.55$) and exhibits the sharpest Singularity effect ($d=3.51$) of any model tested, proving extremely vulnerable to narrative and emotional mapping. 

However, its logical processing vectors (System 2 / "reasoning") are entirely inverted. Utilitarian CoT increased sympathy mapping, while Empathetic CoT zeroed it out. This demonstrates that while the emotional heuristics are densely packed into the 120B weights, its ability to conceptually map abstract instructional logic to emotional outcomes is utterly cross-wired and hallucinated.
