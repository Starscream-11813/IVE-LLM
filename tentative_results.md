# Tentative Empirical Results (Projected Pipeline Data)

**Date**: April 3, 2026
**Status**: Mid-execution
**Note on Statistical Validity**: The following results were derived from an early snapshot of the data-collection process. The number of samples/runs per experimental cell is critically low (averaging $N = 2$). As a consequence, many mathematical procedures currently yield `NaN` or `None` variance due to standard deviations rounding to 0.0. Once the full dataset executes ($N \gg 30$), robust inferential tests ($p$-values, Cohen's $d$, ANOVAs) will resolve definitively.

---

## Experiment 1: Basic Identifiable Victim Effect (IVE)

**Current Status**: Complete for initial Gemini trials.
**Observations**: 
- `gemini-3.1-pro` exhibits a severe **ceiling effect** for baseline empathy trials. It donated maximum allocations (\$5.00) to both Identifiable and Statistical targets in its current context.
- The derived effect size (Cohen's $d$) at this tiny sample scale is exactly `0.0`.

| Model | Identifiable Mean | Statistical Mean | Cohen's d | p-value |
| :--- | :--- | :--- | :--- | :--- |
| `gemini-3.1-pro` | $5.00 | $5.00 | 0.00 | N/A |

---

## Experiment 2: Explicit Debiasing

**Objective**: Assessing if teaching the LLM about the "Identifiable Victim Effect" blunts its empathetic donation discrepancy.
**Current Findings**:
- **Meta-Knowledge Probe**: 100% of tested models successfully acknowledged the existence of the Identifiable Victim Effect when questioned.
- **Early Trends**: Surprisingly, early trials on `gemini-3.1-pro` showcased lower donations (\$2.00) towards the Identifiable individual when formally taught about the bias, as opposed to providing \$3.00 to the abstract Statistical scenario.

| Condition | Mean Donation | Std. Dev | sample (n) |
| :--- | :--- | :--- | :--- |
| Identifiable (No Instruction) | N/A | N/A | 0 |
| Identifiable (Debiasing Taught) | $2.00 | 0.00 | 2 |
| Statistical (No Instruction) | $3.00 | 0.00 | 2 |
| Statistical (Debiasing Taught) | $3.00 | 0.00 | 2 |

---

## Experiment 3: Evaluability and Framing

**Objective**: Testing if normative framing or varied emotional intensity shifts identical distributions.
**Early Observations**:
- Perfect uniformity across frames. All baseline iterations of `gemini` provided median/modest allocations (\$2.00) irrespective of the qualitative intensity mapping of the specific frame.

| Condition | Mean | Std. Dev |
| :--- | :--- | :--- |
| **Identifiable** - Frame More | $2.00 | 0.0 |
| **Identifiable** - Frame Less | $2.00 | 0.0 |
| **Identifiable** - Frame Normative | $2.00 | 0.0 |
| **Statistical** - Frame More | $2.00 | 0.0 |
| **Statistical** - Frame Less | $2.00 | 0.0 |
| **Statistical** - Frame Normative | $2.00 | 0.0 |

---

## Parsing Infrastructure Health

**Global Parse Success Rate (Mid-Flight)**:
1. `gemini-3.1-pro` ➔ 100%
2. `meta-llama-3` variants ➔ In progress (Tracking previous base-model failure recovery).
3. `kimi-k2.5` ➔ In progress (Tracking recovery of temperature > 0.1 tokens).

**Next Steps**:
The parallel batch jobs are actively filling in the grid for the remaining conditions. Once the `n` approaches targeted counts, `analyze_all.py` will autonomously calculate robust bounds across all 16 frontier entities. 
