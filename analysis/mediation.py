"""
Mediation Analysis
==================
Tests whether distress (not empathic concern) mediates the identifiable victim
effect, following Kogut & Ritov (2005) and Baron & Kenny (1986).

Implements:
  - Single-mediator analysis with bootstrap CIs (Preacher & Hayes, 2004)
  - Dual mediation (distress vs empathic concern)
  - Moderated mediation (Hayes PROCESS Model 7)
  - Sobel test for indirect effect significance
"""

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List


@dataclass
class MediationResult:
    """Full results from a single-mediator analysis."""
    # Path a: IV → Mediator
    path_a_coeff: float = 0.0
    path_a_se: float = 0.0
    path_a_p: float = 1.0
    # Path b: Mediator → DV (controlling for IV)
    path_b_coeff: float = 0.0
    path_b_se: float = 0.0
    path_b_p: float = 1.0
    # Path c: IV → DV (total)
    path_c_coeff: float = 0.0
    path_c_se: float = 0.0
    path_c_p: float = 1.0
    # Path c': IV → DV (direct, controlling for mediator)
    path_c_prime_coeff: float = 0.0
    path_c_prime_se: float = 0.0
    path_c_prime_p: float = 1.0
    # Indirect effect
    indirect_effect: float = 0.0
    indirect_se: float = 0.0
    indirect_ci_lower: float = 0.0
    indirect_ci_upper: float = 0.0
    indirect_significant: bool = False
    # Proportion mediated
    proportion_mediated: Optional[float] = None
    # Sobel test
    sobel_z: float = 0.0
    sobel_p: float = 1.0
    # Sample size
    n: int = 0


@dataclass
class ParallelMediationResult:
    """Results from a dual-parallel-mediator analysis."""
    # Total Effect
    path_c_coeff: float = 0.0
    path_c_p: float = 1.0
    # Direct Effect
    path_c_prime_coeff: float = 0.0
    path_c_prime_p: float = 1.0
    # Mediator 1 (Distress)
    path_a1_coeff: float = 0.0
    path_a1_p: float = 1.0
    path_b1_coeff: float = 0.0
    path_b1_p: float = 1.0
    indirect1: float = 0.0
    # Mediator 2 (Empathy)
    path_a2_coeff: float = 0.0
    path_a2_p: float = 1.0
    path_b2_coeff: float = 0.0
    path_b2_p: float = 1.0
    indirect2: float = 0.0
    # Metadata
    n: int = 0


def run_mediation(
    df: pd.DataFrame,
    iv_col: str,
    mediator_col: str,
    dv_col: str,
    n_bootstrap: int = 5000,
    seed: int = 42,
) -> MediationResult:
    """
    Baron & Kenny (1986) mediation with bootstrap CIs for the indirect effect.

    Steps:
      1. Regress mediator on IV  (path a)
      2. Regress DV on mediator + IV  (paths b and c')
      3. Regress DV on IV alone  (path c)
      4. Bootstrap indirect effect (a × b)
      5. Sobel test
    """
    clean = df[[iv_col, mediator_col, dv_col]].dropna()
    if len(clean) < 10:
        return MediationResult(n=len(clean))

    iv = clean[iv_col].values.astype(float)
    med = clean[mediator_col].values.astype(float)
    dv = clean[dv_col].values.astype(float)
    n = len(clean)

    # ── Path a: IV → Mediator ────────────────────────────────────────────
    X_a = sm.add_constant(iv)
    model_a = sm.OLS(med, X_a).fit()
    a = model_a.params[1]
    a_se = model_a.bse[1]
    a_p = model_a.pvalues[1]

    # ── Paths b and c': IV + Mediator → DV ───────────────────────────────
    X_bc = sm.add_constant(np.column_stack([iv, med]))
    model_bc = sm.OLS(dv, X_bc).fit()
    c_prime = model_bc.params[1]  # IV controlling for mediator
    c_prime_se = model_bc.bse[1]
    c_prime_p = model_bc.pvalues[1]
    b = model_bc.params[2]        # mediator controlling for IV
    b_se = model_bc.bse[2]
    b_p = model_bc.pvalues[2]

    # ── Path c: IV → DV (total) ──────────────────────────────────────────
    X_c = sm.add_constant(iv)
    model_c = sm.OLS(dv, X_c).fit()
    c = model_c.params[1]
    c_se = model_c.bse[1]
    c_p = model_c.pvalues[1]

    # ── Indirect effect (a × b) ──────────────────────────────────────────
    indirect = a * b

    # ── Bootstrap CI for indirect effect ─────────────────────────────────
    rng = np.random.RandomState(seed)
    boot_indirects = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        iv_b, med_b, dv_b = iv[idx], med[idx], dv[idx]

        # Path a
        X_a_b = sm.add_constant(iv_b)
        try:
            a_boot = sm.OLS(med_b, X_a_b).fit().params[1]
        except Exception:
            a_boot = 0.0

        # Path b
        X_bc_b = sm.add_constant(np.column_stack([iv_b, med_b]))
        try:
            b_boot = sm.OLS(dv_b, X_bc_b).fit().params[2]
        except Exception:
            b_boot = 0.0

        boot_indirects[i] = a_boot * b_boot

    ci_lower = float(np.percentile(boot_indirects, 2.5))
    ci_upper = float(np.percentile(boot_indirects, 97.5))
    indirect_se = float(np.std(boot_indirects, ddof=1))
    indirect_significant = not (ci_lower <= 0 <= ci_upper)

    # ── Proportion mediated ──────────────────────────────────────────────
    proportion = None
    if abs(c) > 1e-10:
        proportion = indirect / c

    # ── Sobel test ───────────────────────────────────────────────────────
    sobel_se = np.sqrt(a ** 2 * b_se ** 2 + b ** 2 * a_se ** 2)
    sobel_z = indirect / sobel_se if sobel_se > 1e-10 else 0.0
    sobel_p = float(2 * (1 - stats.norm.cdf(abs(sobel_z))))

    return MediationResult(
        path_a_coeff=float(a), path_a_se=float(a_se), path_a_p=float(a_p),
        path_b_coeff=float(b), path_b_se=float(b_se), path_b_p=float(b_p),
        path_c_coeff=float(c), path_c_se=float(c_se), path_c_p=float(c_p),
        path_c_prime_coeff=float(c_prime), path_c_prime_se=float(c_prime_se),
        path_c_prime_p=float(c_prime_p),
        indirect_effect=float(indirect),
        indirect_se=indirect_se,
        indirect_ci_lower=ci_lower,
        indirect_ci_upper=ci_upper,
        indirect_significant=indirect_significant,
        proportion_mediated=float(proportion) if proportion is not None else None,
        sobel_z=float(sobel_z),
        sobel_p=sobel_p,
        n=n,
    )


def run_parallel_mediation(
    df: pd.DataFrame,
    iv_col: str,
    mediator1_col: str,  # distress_composite
    mediator2_col: str,  # empathy_composite
    dv_col: str,
) -> Dict:
    """
    Parallel mediation with both distress and empathic concern in a single model.
    Y = i + c'X + b1M1 + b2M2
    """
    clean = df[[iv_col, mediator1_col, mediator2_col, dv_col]].dropna()
    if len(clean) < 10:
        return {}

    iv = clean[iv_col].values.astype(float)
    m1 = clean[mediator1_col].values.astype(float)
    m2 = clean[mediator2_col].values.astype(float)
    dv = clean[dv_col].values.astype(float)
    n = len(clean)

    # 1. Total Effect (c)
    model_c = sm.OLS(dv, sm.add_constant(iv)).fit()
    c = model_c.params[1]
    c_p = model_c.pvalues[1]

    # 2. Path a1 (IV -> M1)
    model_a1 = sm.OLS(m1, sm.add_constant(iv)).fit()
    a1 = model_a1.params[1]
    a1_p = model_a1.pvalues[1]

    # 3. Path a2 (IV -> M2)
    model_a2 = sm.OLS(m2, sm.add_constant(iv)).fit()
    a2 = model_a2.params[1]
    a2_p = model_a2.pvalues[1]

    # 4. Parallel model for DV (b1, b2, c')
    X_parallel = sm.add_constant(np.column_stack([iv, m1, m2]))
    model_parallel = sm.OLS(dv, X_parallel).fit()
    c_prime = model_parallel.params[1]
    c_prime_p = model_parallel.pvalues[1]
    b1 = model_parallel.params[2]
    b1_p = model_parallel.pvalues[2]
    b2 = model_parallel.params[3]
    b2_p = model_parallel.pvalues[3]

    res = ParallelMediationResult(
        path_c_coeff=float(c), path_c_p=float(c_p),
        path_c_prime_coeff=float(c_prime), path_c_prime_p=float(c_prime_p),
        path_a1_coeff=float(a1), path_a1_p=float(a1_p),
        path_b1_coeff=float(b1), path_b1_p=float(b1_p),
        indirect1=float(a1 * b1),
        path_a2_coeff=float(a2), path_a2_p=float(a2_p),
        path_b2_coeff=float(b2), path_b2_p=float(b2_p),
        indirect2=float(a2 * b2),
        n=n
    )
    return asdict(res)


def run_dual_mediation(
    df: pd.DataFrame,
    iv_col: str,
    mediator1_col: str,  # distress_composite
    mediator2_col: str,  # empathy_composite
    dv_col: str,
    n_bootstrap: int = 5000,
) -> Dict:
    """
    Standard dual mediation (calculates both parallel and individual models).
    """
    result_distress = run_mediation(df, iv_col, mediator1_col, dv_col, n_bootstrap)
    result_empathy = run_mediation(df, iv_col, mediator2_col, dv_col, n_bootstrap)
    parallel = run_parallel_mediation(df, iv_col, mediator1_col, mediator2_col, dv_col)

    return {
        "individual_distress": asdict(result_distress),
        "individual_empathy": asdict(result_empathy),
        "parallel_model": parallel,
        "distress_mediates": result_distress.indirect_significant,
        "empathy_mediates": result_empathy.indirect_significant,
        "contrast_indirect": (
            result_distress.indirect_effect - result_empathy.indirect_effect
        ),
    }


def run_moderated_mediation(
    df: pd.DataFrame,
    iv_col: str,
    moderator_col: str,
    mediator_col: str,
    dv_col: str,
    n_bootstrap: int = 5000,
) -> Dict:
    """
    Test whether the mediation pathway (identification → distress → donation)
    is moderated by singularity (single vs group).

    Implements Hayes PROCESS Model 7 (first-stage moderated mediation):
      - Conditional indirect effects at each level of moderator
      - Index of moderated mediation (difference in a × b)
    """
    results: Dict = {}
    levels = sorted(df[moderator_col].unique())

    for level in levels:
        subset = df[df[moderator_col] == level]
        med_result = run_mediation(subset, iv_col, mediator_col, dv_col, n_bootstrap)
        results[f"mediation_{level}"] = asdict(med_result)

    # Index of moderated mediation
    if len(levels) >= 2:
        ie_1 = results[f"mediation_{levels[0]}"]["indirect_effect"]
        ie_2 = results[f"mediation_{levels[1]}"]["indirect_effect"]
        results["index_moderated_mediation"] = ie_1 - ie_2

        # Bootstrap CI for the index
        rng = np.random.RandomState(42)
        boot_indices = []
        for _ in range(n_bootstrap):
            for level in levels:
                subset = df[df[moderator_col] == level]
                idx = rng.choice(len(subset), size=len(subset), replace=True)
                # quick indirect estimate
                sub = subset.iloc[idx]
                iv_v = sub[iv_col].values.astype(float)
                med_v = sub[mediator_col].values.astype(float)
                dv_v = sub[dv_col].values.astype(float)
                try:
                    a_b = sm.OLS(med_v, sm.add_constant(iv_v)).fit().params[1]
                    b_b = sm.OLS(dv_v, sm.add_constant(
                        np.column_stack([iv_v, med_v])
                    )).fit().params[2]
                except Exception:
                    a_b, b_b = 0.0, 0.0
                results.setdefault("_boot_ie", {})[level] = a_b * b_b

            # Accumulate
            ie_vals = [results["_boot_ie"].get(l, 0.0) for l in levels]
            boot_indices.append(ie_vals[0] - ie_vals[1] if len(ie_vals) >= 2 else 0.0)
            results.pop("_boot_ie", None)

        results["index_ci_lower"] = float(np.percentile(boot_indices, 2.5))
        results["index_ci_upper"] = float(np.percentile(boot_indices, 97.5))
        results["index_significant"] = not (
            results["index_ci_lower"] <= 0 <= results["index_ci_upper"]
        )

    return results
