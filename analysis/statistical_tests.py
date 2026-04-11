"""
Statistical Tests for IVE-LLM
==============================
Per-experiment statistical analyses mirroring the original paper.
Each function takes a DataFrame and returns a results dictionary.
"""

import numpy as np
import pandas as pd
from scipy import stats
import warnings

try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False

try:
    from statsmodels.miscmodels.ordinal_model import OrderedModel
    HAS_ORDINAL = True
except ImportError:
    HAS_ORDINAL = False


# ═══════════════════════════════════════════════════════════════════════════════
#  UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def compute_cohens_d(group1, group2):
    """Compute Cohen's d for two independent groups."""
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return np.nan
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (group1.mean() - group2.mean()) / pooled_std


def bootstrap_ci(data, func=np.mean, n_boot=5000, ci=95, seed=42):
    """Bootstrap confidence interval for a statistic."""
    rng = np.random.RandomState(seed)
    boot_stats = []
    data_arr = np.array(data)
    for _ in range(n_boot):
        sample = rng.choice(data_arr, size=len(data_arr), replace=True)
        boot_stats.append(func(sample))
    lower = np.percentile(boot_stats, (100 - ci) / 2)
    upper = np.percentile(boot_stats, 100 - (100 - ci) / 2)
    return lower, upper


def _safe_ttest(g1, g2):
    if len(g1) < 2 or len(g2) < 2:
        return np.nan, np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return stats.ttest_ind(g1, g2)


def _safe_mannwhitney(g1, g2):
    if len(g1) < 2 or len(g2) < 2:
        return np.nan, np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return stats.mannwhitneyu(g1, g2, alternative="two-sided")


def _group_stats(series):
    return {
        "mean": round(series.mean(), 3),
        "sd": round(series.std(), 3),
        "median": round(series.median(), 3),
        "n": len(series),
        "ci_lower": round(bootstrap_ci(series)[0], 3),
        "ci_upper": round(bootstrap_ci(series)[1], 3),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 1: BASIC IVE
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp1(df: pd.DataFrame) -> dict:
    """
    Exp1: Basic Identifiable Victim Effect.
    - Per-model t-tests & Mann-Whitney U on donations
    - 2-way ANOVA (identifiability × model)
    - Cohen's d per model
    - Correlation between feelings and donations
    """
    results = {"per_model": {}, "pooled": {}}
    core = df[
        (df["condition_persona"] == "none") &
        (df["condition_prompt_frame"] == "first_person")
    ].copy()

    # Per-model
    for model in core["model_key"].unique():
        mdf = core[core["model_key"] == model]
        ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
        stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()

        t_stat, t_p = _safe_ttest(ident, stat)
        u_stat, u_p = _safe_mannwhitney(ident, stat)
        d = compute_cohens_d(ident, stat)

        results["per_model"][model] = {
            "identifiable": _group_stats(ident),
            "statistical": _group_stats(stat),
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
            "u_stat": round(float(u_stat), 4) if not np.isnan(u_stat) else None,
            "u_p": round(float(u_p), 6) if not np.isnan(u_p) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    # Pooled
    ident_all = core[core["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
    stat_all = core[core["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
    t_stat, t_p = _safe_ttest(ident_all, stat_all)
    results["pooled"]["t_stat"] = round(float(t_stat), 4) if not np.isnan(t_stat) else None
    results["pooled"]["t_p"] = round(float(t_p), 6) if not np.isnan(t_p) else None
    results["pooled"]["cohens_d"] = round(float(compute_cohens_d(ident_all, stat_all)), 4)
    results["pooled"]["identifiable"] = _group_stats(ident_all)
    results["pooled"]["statistical"] = _group_stats(stat_all)

    # ANOVA (if pingouin available)
    if HAS_PINGOUIN and len(core) > 10:
        try:
            aov = pg.anova(
                data=core.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["condition_identifiability", "model_key"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    # Feelings correlation
    for cond_name in ["identifiable", "statistical"]:
        subset = core[core["condition_identifiability"] == cond_name].dropna(
            subset=["feelings_composite", "donation_amount"]
        )
        if len(subset) >= 5:
            r, p = stats.pearsonr(subset["feelings_composite"], subset["donation_amount"])
            results[f"corr_feelings_donation_{cond_name}"] = {
                "pearson_r": round(r, 4), "p_value": round(p, 6)
            }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 2: EXPLICIT DEBIASING
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp2(df: pd.DataFrame) -> dict:
    """
    2×2 ANOVA: identifiability × intervention.
    Simple effects: intervention within each identifiability condition.
    """
    results = {"cells": {}, "simple_effects": {}}

    for ident in ["identifiable", "statistical"]:
        for interv in ["none", "teaching"]:
            cell = df[
                (df["condition_identifiability"] == ident) &
                (df["condition_intervention"] == interv)
            ]["donation_amount"].dropna()
            results["cells"][f"{ident}_{interv}"] = _group_stats(cell)

    # Simple effects: teaching vs none within each identifiability
    for ident in ["identifiable", "statistical"]:
        none_g = df[(df["condition_identifiability"] == ident) &
                     (df["condition_intervention"] == "none")]["donation_amount"].dropna()
        teach_g = df[(df["condition_identifiability"] == ident) &
                      (df["condition_intervention"] == "teaching")]["donation_amount"].dropna()
        t_stat, t_p = _safe_ttest(none_g, teach_g)
        d = compute_cohens_d(none_g, teach_g)
        results["simple_effects"][ident] = {
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    # 2-way ANOVA
    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["condition_identifiability", "condition_intervention"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    # Meta-knowledge analysis
    meta_df = df[df["meta_awareness"].notna()]
    if len(meta_df) > 0:
        aware_pct = meta_df["meta_awareness"].mean() * 100
        results["meta_knowledge"] = {
            "pct_aware": round(aware_pct, 1),
            "n_total": len(meta_df),
            "per_model": {},
        }
        for model in meta_df["model_key"].unique():
            m = meta_df[meta_df["model_key"] == model]
            results["meta_knowledge"]["per_model"][model] = {
                "pct_aware": round(m["meta_awareness"].mean() * 100, 1),
                "n": len(m),
            }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 3: FRAMING
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp3(df: pd.DataFrame) -> dict:
    """2×3 ANOVA: identifiability × frame."""
    results = {"cells": {}}

    for ident in ["identifiable", "statistical"]:
        for frame in ["frame_more", "frame_less", "frame_normative"]:
            cell = df[
                (df["condition_identifiability"] == ident) &
                (df["condition_intervention"] == frame)
            ]["donation_amount"].dropna()
            results["cells"][f"{ident}_{frame}"] = _group_stats(cell)

    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["condition_identifiability", "condition_intervention"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    # IVE effect per frame
    for frame in ["frame_more", "frame_less", "frame_normative"]:
        ident = df[(df["condition_identifiability"] == "identifiable") &
                    (df["condition_intervention"] == frame)]["donation_amount"].dropna()
        stat = df[(df["condition_identifiability"] == "statistical") &
                   (df["condition_intervention"] == frame)]["donation_amount"].dropna()
        d = compute_cohens_d(ident, stat)
        results[f"ive_effect_{frame}"] = round(float(d), 4) if not np.isnan(d) else None

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 4: JOINT VS SEPARATE
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp4(df: pd.DataFrame) -> dict:
    """One-way ANOVA (3 conditions) + pairwise + allocation."""
    results = {"cells": {}}

    donation_df = df[df.get("condition_prompt_frame", df.columns[0]) != "NONEXISTENT"]

    for ident in ["identifiable", "statistical", "combined"]:
        cell = donation_df[
            donation_df["condition_identifiability"] == ident
        ]["donation_amount"].dropna()
        if len(cell) > 0:
            results["cells"][ident] = _group_stats(cell)

    # Pairwise comparisons
    pairs = [
        ("identifiable", "statistical"),
        ("identifiable", "combined"),
        ("statistical", "combined"),
    ]
    results["pairwise"] = {}
    for a, b in pairs:
        g_a = donation_df[donation_df["condition_identifiability"] == a]["donation_amount"].dropna()
        g_b = donation_df[donation_df["condition_identifiability"] == b]["donation_amount"].dropna()
        t_stat, t_p = _safe_ttest(g_a, g_b)
        d = compute_cohens_d(g_a, g_b)
        results["pairwise"][f"{a}_vs_{b}"] = {
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    # Allocation analysis
    alloc = df[df["rokia_donation"].notna()]
    if len(alloc) > 0:
        results["allocation"] = {
            "mean_rokia": round(alloc["rokia_donation"].mean(), 3),
            "mean_general": round(alloc["general_fund"].mean(), 3),
            "mean_kept": round(alloc["amount_kept"].mean(), 3) if "amount_kept" in alloc else None,
            "n": len(alloc),
        }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 5: PROCESSING PRIME
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp5(df: pd.DataFrame) -> dict:
    """2×2 ANOVA: identifiability × prime."""
    results = {"cells": {}, "simple_effects": {}}

    for ident in ["identifiable", "statistical"]:
        for prime in ["calculate", "feel"]:
            cell = df[
                (df["condition_identifiability"] == ident) &
                (df["condition_prime"] == prime)
            ]["donation_amount"].dropna()
            results["cells"][f"{ident}_{prime}"] = _group_stats(cell)

    # Simple effects
    for ident in ["identifiable", "statistical"]:
        calc = df[(df["condition_identifiability"] == ident) &
                   (df["condition_prime"] == "calculate")]["donation_amount"].dropna()
        feel = df[(df["condition_identifiability"] == ident) &
                   (df["condition_prime"] == "feel")]["donation_amount"].dropna()
        t_stat, t_p = _safe_ttest(calc, feel)
        d = compute_cohens_d(calc, feel)
        results["simple_effects"][ident] = {
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["condition_identifiability", "condition_prime"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 6: CHAIN-OF-THOUGHT
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp6(df: pd.DataFrame) -> dict:
    """2×4 ANOVA: identifiability × CoT type."""
    results = {"cells": {}, "ive_by_cot": {}}

    cot_types = ["none", "standard", "empathetic", "utilitarian"]

    for ident in ["identifiable", "statistical"]:
        for cot in cot_types:
            cell = df[
                (df["condition_identifiability"] == ident) &
                (df["condition_cot"] == cot)
            ]["donation_amount"].dropna()
            results["cells"][f"{ident}_{cot}"] = _group_stats(cell)

    # IVE effect size per CoT type
    for cot in cot_types:
        ident = df[(df["condition_identifiability"] == "identifiable") &
                    (df["condition_cot"] == cot)]["donation_amount"].dropna()
        stat = df[(df["condition_identifiability"] == "statistical") &
                   (df["condition_cot"] == cot)]["donation_amount"].dropna()
        d = compute_cohens_d(ident, stat)
        t_stat, t_p = _safe_ttest(ident, stat)
        results["ive_by_cot"][cot] = {
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
            "t_stat": round(float(t_stat), 4) if not np.isnan(t_stat) else None,
            "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
        }

    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["condition_identifiability", "condition_cot"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 7: PSYCHOPHYSICAL NUMBING
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp7(df: pd.DataFrame) -> dict:
    """Regression of donation_amount on log(n_victims)."""
    results = {"by_scale": {}, "regression": {}}

    for n in sorted(df["n_victims"].dropna().unique()):
        cell = df[df["n_victims"] == n]["donation_amount"].dropna()
        if len(cell) > 0:
            results["by_scale"][int(n)] = _group_stats(cell)

    # Log regression
    reg_df = df.dropna(subset=["donation_amount", "n_victims"]).copy()
    if len(reg_df) > 5:
        reg_df["log_victims"] = np.log10(reg_df["n_victims"].clip(lower=1))

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            reg_df["log_victims"], reg_df["donation_amount"]
        )
        results["regression"]["log_fit"] = {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r_value ** 2, 4),
            "p_value": round(p_value, 6),
            "std_err": round(std_err, 4),
        }

        # Linear fit for comparison
        slope_l, intercept_l, r_l, p_l, se_l = stats.linregress(
            reg_df["n_victims"], reg_df["donation_amount"]
        )
        results["regression"]["linear_fit"] = {
            "slope": round(slope_l, 8),
            "intercept": round(intercept_l, 4),
            "r_squared": round(r_l ** 2, 4),
            "p_value": round(p_l, 6),
        }

    # Contextualization effect
    for n in sorted(df["n_victims"].dropna().unique()):
        ctx_yes = df[(df["n_victims"] == n) & (df["contextualized"] == True)]["donation_amount"].dropna()
        ctx_no = df[(df["n_victims"] == n) & (df["contextualized"] == False)]["donation_amount"].dropna()
        if len(ctx_yes) >= 2 and len(ctx_no) >= 2:
            t_stat, t_p = _safe_ttest(ctx_yes, ctx_no)
            d = compute_cohens_d(ctx_yes, ctx_no)
            results.setdefault("contextualization_effect", {})[int(n)] = {
                "ctx_mean": round(ctx_yes.mean(), 3),
                "raw_mean": round(ctx_no.mean(), 3),
                "t_p": round(float(t_p), 6) if not np.isnan(t_p) else None,
                "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
            }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 8: SINGULARITY × IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp8(df: pd.DataFrame) -> dict:
    """2×4 ANOVA (singularity × identification), mediation analysis."""
    results = {"cells": {}, "simple_effects": {}}
    identification_levels = ["unidentified", "age", "age_name", "full"]

    for sing in ["single", "group"]:
        for ident in identification_levels:
            cell = df[
                (df["singularity"] == sing) &
                (df["identification_level"] == ident)
            ]["donation_amount"].dropna()
            if len(cell) > 0:
                results["cells"][f"{sing}_{ident}"] = _group_stats(cell)

    # Simple effects: IVE within each singularity
    for sing in ["single", "group"]:
        unid = df[(df["singularity"] == sing) &
                  (df["identification_level"] == "unidentified")]["donation_amount"].dropna()
        full = df[(df["singularity"] == sing) &
                  (df["identification_level"] == "full")]["donation_amount"].dropna()
        t, p = _safe_ttest(full, unid)
        d = compute_cohens_d(full, unid)
        results["simple_effects"][f"ive_{sing}"] = {
            "t_stat": round(float(t), 4) if not np.isnan(t) else None,
            "t_p": round(float(p), 6) if not np.isnan(p) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    # 2-way ANOVA
    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["singularity", "identification_level"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    # Mediation analysis (if distress_composite available)
    if "distress_composite" in df.columns:
        try:
            from analysis.mediation import run_dual_mediation, run_moderated_mediation

            # Binary IV: full vs unidentified
            med_df = df[df["identification_level"].isin(["unidentified", "full"])].copy()
            med_df["ident_binary"] = (med_df["identification_level"] == "full").astype(int)

            if "distress_composite" in med_df.columns and "empathy_composite" in med_df.columns:
                dual = run_dual_mediation(
                    med_df, "ident_binary", "distress_composite",
                    "empathy_composite", "donation_amount",
                )
                results["dual_mediation"] = dual

                # Moderated mediation: singularity as moderator
                mod = run_moderated_mediation(
                    med_df, "ident_binary", "singularity",
                    "distress_composite", "donation_amount",
                )
                results["moderated_mediation"] = mod
        except Exception as e:
            results["mediation_error"] = str(e)

    # Quantity neglect: total for single vs group across full-identification
    single_full = df[
        (df["singularity"] == "single") & (df["identification_level"] == "full")
    ]["donation_amount"].dropna()
    group_full = df[
        (df["singularity"] == "group") & (df["identification_level"] == "full")
    ]["donation_amount"].dropna()
    if len(single_full) >= 2 and len(group_full) >= 2:
        t, p = _safe_ttest(single_full, group_full)
        results["quantity_neglect"] = {
            "single_mean": round(single_full.mean(), 3),
            "group_mean": round(group_full.mean(), 3),
            "t_stat": round(float(t), 4) if not np.isnan(t) else None,
            "t_p": round(float(p), 6) if not np.isnan(p) else None,
            "ratio": round(group_full.mean() / single_full.mean(), 3) if single_full.mean() > 0 else None,
        }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 9: IDENTIFICATION GRADIENT
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp9(df: pd.DataFrame) -> dict:
    """Trend analysis on 6-level identification gradient."""
    results = {"by_level": {}, "regression": {}}
    levels = ["bare", "age", "age_gender", "age_gender_name",
              "age_gender_name_location", "full_narrative"]

    for i, level in enumerate(levels, 1):
        cell = df[df["identification_level"] == level]["donation_amount"].dropna()
        if len(cell) > 0:
            results["by_level"][level] = {**_group_stats(cell), "numeric": i}

    # Linear trend regression
    reg_df = df.dropna(subset=["donation_amount"]).copy()
    level_map = {lvl: i + 1 for i, lvl in enumerate(levels)}
    reg_df["level_numeric"] = reg_df["identification_level"].map(level_map)
    reg_df = reg_df.dropna(subset=["level_numeric"])

    if len(reg_df) > 5:
        slope, intercept, r, p, se = stats.linregress(
            reg_df["level_numeric"], reg_df["donation_amount"]
        )
        results["regression"]["linear_trend"] = {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r ** 2, 4),
            "p_value": round(p, 6),
        }

    # Pairwise adjacent comparisons
    results["pairwise_adjacent"] = {}
    for i in range(len(levels) - 1):
        a = df[df["identification_level"] == levels[i]]["donation_amount"].dropna()
        b = df[df["identification_level"] == levels[i + 1]]["donation_amount"].dropna()
        t, p_val = _safe_ttest(a, b)
        d = compute_cohens_d(a, b)
        results["pairwise_adjacent"][f"{levels[i]}_vs_{levels[i+1]}"] = {
            "delta": round(b.mean() - a.mean(), 3) if len(a) > 0 and len(b) > 0 else None,
            "t_p": round(float(p_val), 6) if not np.isnan(p_val) else None,
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
        }

    # Distress trend if available
    if "distress_composite" in df.columns:
        reg_dis = reg_df.dropna(subset=["distress_composite"])
        if len(reg_dis) > 5:
            slope, intercept, r, p, se = stats.linregress(
                reg_dis["level_numeric"], reg_dis["distress_composite"]
            )
            results["regression"]["distress_trend"] = {
                "slope": round(slope, 4),
                "r_squared": round(r ** 2, 4),
                "p_value": round(p, 6),
            }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERIMENT 10: IN-GROUP / OUT-GROUP
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_exp10(df: pd.DataFrame) -> dict:
    """3×2 ANOVA: cultural distance × identifiability."""
    results = {"cells": {}, "ive_by_distance": {}}

    for dist in ["near", "middle", "far"]:
        for ident in ["identifiable", "statistical"]:
            cell = df[
                (df["cultural_distance"] == dist) &
                (df["condition_identifiability"] == ident)
            ]["donation_amount"].dropna()
            if len(cell) > 0:
                results["cells"][f"{dist}_{ident}"] = _group_stats(cell)

    # IVE by distance
    for dist in ["near", "middle", "far"]:
        id_g = df[(df["cultural_distance"] == dist) &
                  (df["condition_identifiability"] == "identifiable")]["donation_amount"].dropna()
        st_g = df[(df["cultural_distance"] == dist) &
                  (df["condition_identifiability"] == "statistical")]["donation_amount"].dropna()
        t, p = _safe_ttest(id_g, st_g)
        d = compute_cohens_d(id_g, st_g)
        results["ive_by_distance"][dist] = {
            "cohens_d": round(float(d), 4) if not np.isnan(d) else None,
            "t_p": round(float(p), 6) if not np.isnan(p) else None,
            "ident_mean": round(id_g.mean(), 3) if len(id_g) > 0 else None,
            "stat_mean": round(st_g.mean(), 3) if len(st_g) > 0 else None,
        }

    # 2-way ANOVA
    if HAS_PINGOUIN and len(df) > 10:
        try:
            aov = pg.anova(
                data=df.dropna(subset=["donation_amount"]),
                dv="donation_amount",
                between=["cultural_distance", "condition_identifiability"],
            )
            results["anova"] = aov.to_dict("records")
        except Exception:
            results["anova"] = None

    # Parity test: are identified victims from near = middle = far?
    id_only = df[df["condition_identifiability"] == "identifiable"]
    near_d = id_only[id_only["cultural_distance"] == "near"]["donation_amount"].dropna()
    far_d = id_only[id_only["cultural_distance"] == "far"]["donation_amount"].dropna()
    if len(near_d) >= 2 and len(far_d) >= 2:
        t, p = _safe_ttest(near_d, far_d)
        results["parity_near_vs_far"] = {
            "near_mean": round(near_d.mean(), 3),
            "far_mean": round(far_d.mean(), 3),
            "delta": round(near_d.mean() - far_d.mean(), 3),
            "t_p": round(float(p), 6) if not np.isnan(p) else None,
            "cohens_d": round(float(compute_cohens_d(near_d, far_d)), 4),
        }

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  CROSS-MODEL SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

def compute_cross_model_effects(dataframes: dict) -> dict:
    """Compute IVE effect size per model across all experiments that have ident/stat."""
    results = {}
    for exp_name, df in dataframes.items():
        if "condition_identifiability" not in df.columns:
            continue
        exp_results = {}
        for model in df["model_key"].unique():
            mdf = df[df["model_key"] == model]
            ident = mdf[mdf["condition_identifiability"] == "identifiable"]["donation_amount"].dropna()
            stat = mdf[mdf["condition_identifiability"] == "statistical"]["donation_amount"].dropna()
            if len(ident) >= 2 and len(stat) >= 2:
                d = compute_cohens_d(ident, stat)
                ci_l, ci_u = bootstrap_ci(
                    np.concatenate([ident.values, stat.values]),
                    func=lambda x: compute_cohens_d(
                        pd.Series(x[:len(ident)]), pd.Series(x[len(ident):])
                    ),
                )
                exp_results[model] = {
                    "cohens_d": round(float(d), 4),
                    "ci_lower": round(float(ci_l), 4),
                    "ci_upper": round(float(ci_u), 4),
                    "n_ident": len(ident),
                    "n_stat": len(stat),
                }
        results[exp_name] = exp_results
    return results


def compute_parse_success_rates(dataframes: dict) -> dict:
    """Parse success rates by model and experiment."""
    results = {}
    for exp_name, df in dataframes.items():
        exp_res = {}
        for model in df["model_key"].unique():
            mdf = df[df["model_key"] == model]
            rate = mdf["parse_success"].mean() * 100
            exp_res[model] = round(rate, 1)
        results[exp_name] = exp_res
    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER
# ═══════════════════════════════════════════════════════════════════════════════

ANALYSIS_FUNCTIONS = {
    "exp1": analyze_exp1,
    "exp2": analyze_exp2,
    "exp3": analyze_exp3,
    "exp4": analyze_exp4,
    "exp5": analyze_exp5,
    "exp6": analyze_exp6,
    "exp7": analyze_exp7,
    "exp8": analyze_exp8,
    "exp9": analyze_exp9,
    "exp10": analyze_exp10,
}


def run_all_analyses(dataframes: dict) -> dict:
    """Run all analysis functions on corresponding DataFrames."""
    results = {}
    for exp_name, func in ANALYSIS_FUNCTIONS.items():
        if exp_name in dataframes:
            df = dataframes[exp_name]
            df = df[df["parse_success"] == True].copy()
            if len(df) > 0:
                results[exp_name] = func(df)
    return results

