"""Small, dependency-light toolkit for analysing A/B tests on conversion-type metrics."""
import numpy as np
from scipy import stats


def srm_test(n_control: int, n_treatment: int, expected_ratio: float = 0.5):
    """Sample-ratio-mismatch check: chi-square test of the observed split against the planned split."""
    total = n_control + n_treatment
    expected = [total * expected_ratio, total * (1 - expected_ratio)]
    chi2, p = stats.chisquare([n_control, n_treatment], expected)
    return {"chi2": chi2, "p_value": p, "control_share": n_control / total}


def two_proportion_test(x_c, n_c, x_t, n_t, alpha=0.05):
    """Two-sided z-test for a difference in proportions (treatment - control) with a Wald CI."""
    p_c, p_t = x_c / n_c, x_t / n_t
    p_pool = (x_c + x_t) / (n_c + n_t)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
    z = (p_t - p_c) / se_pool
    p_value = 2 * stats.norm.sf(abs(z))
    se = np.sqrt(p_c * (1 - p_c) / n_c + p_t * (1 - p_t) / n_t)
    zc = stats.norm.ppf(1 - alpha / 2)
    diff = p_t - p_c
    return {"control": p_c, "treatment": p_t, "diff": diff, "rel_lift": diff / p_c,
            "ci_low": diff - zc * se, "ci_high": diff + zc * se, "z": z, "p_value": p_value}


def bootstrap_diff(control: np.ndarray, treatment: np.ndarray, n_boot=5000, seed=42):
    """Bootstrap distribution of mean(treatment) - mean(control)."""
    rng = np.random.default_rng(seed)
    c_means = rng.binomial(len(control), control.mean(), n_boot) / len(control) if set(np.unique(control)) <= {0, 1} \
        else np.array([rng.choice(control, len(control)).mean() for _ in range(n_boot)])
    t_means = rng.binomial(len(treatment), treatment.mean(), n_boot) / len(treatment) if set(np.unique(treatment)) <= {0, 1} \
        else np.array([rng.choice(treatment, len(treatment)).mean() for _ in range(n_boot)])
    return t_means - c_means


def mde_two_proportion(p_base, n_per_group, alpha=0.05, power=0.8):
    """Minimum detectable absolute difference for a two-sided test with equal groups."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return z * np.sqrt(2 * p_base * (1 - p_base) / n_per_group)


def sample_size_two_proportion(p_base, abs_diff, alpha=0.05, power=0.8):
    """Users needed per group to detect `abs_diff` from baseline `p_base`."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    p2 = p_base + abs_diff
    var = p_base * (1 - p_base) + p2 * (1 - p2)
    return int(np.ceil(z ** 2 * var / abs_diff ** 2))
