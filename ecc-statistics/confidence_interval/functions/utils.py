"""
Otter Grader utilities for the Confidence Interval notebook.
Run run_tests(globals()) from the notebook after completing the exercises.
"""

import numpy as np
from scipy import stats
import otter

grader = otter.Notebook()


def run_tests(env):
    """
    Run all exercise tests using variables from the notebook namespace.
    Call from the notebook as: run_tests(globals())
    """
    print("Running tests...\n")

    try:
        _test_exercise1(env)
        print("Exercise 1: ✅ Passed")
    except Exception as e:
        print(f"Exercise 1: ❌ {e}")

    try:
        _test_exercise2(env)
        print("Exercise 2: ✅ Passed")
    except Exception as e:
        print(f"Exercise 2: ❌ {e}")

    try:
        _test_exercise3(env)
        print("Exercise 3: ✅ Passed")
    except Exception as e:
        print(f"Exercise 3: ❌ {e}")

    print("\nAll tests completed. Great work!")


def _test_exercise1(env):
    """Check z, ci_lower, ci_upper for the 95% CI formula."""
    z = env.get("z")
    ci_lower = env.get("ci_lower")
    ci_upper = env.get("ci_upper")
    n = env.get("n")
    sample_mean = env.get("sample_mean")
    sample_std = env.get("sample_std")

    if z is None or ci_lower is None or ci_upper is None:
        raise AssertionError("Define z, ci_lower, and ci_upper in the Exercise 1 cell.")

    if n is None or sample_mean is None or sample_std is None:
        raise AssertionError("Run the earlier cells that define n, sample_mean, and sample_std.")

    # Expected z for 95% two-tailed
    alpha = 0.05
    expected_z = stats.norm.ppf(1 - alpha / 2)
    if not np.isclose(z, expected_z, atol=1e-5):
        raise AssertionError(
            f"z should be the 97.5% quantile of the standard normal (about {expected_z:.4f}). "
            "Use stats.norm.ppf(1 - alpha/2)."
        )

    standard_error = sample_std / np.sqrt(n)
    expected_lower = sample_mean - z * standard_error
    expected_upper = sample_mean + z * standard_error

    if not np.isclose(ci_lower, expected_lower, atol=1e-5):
        raise AssertionError("ci_lower should equal sample_mean - z * standard_error.")
    if not np.isclose(ci_upper, expected_upper, atol=1e-5):
        raise AssertionError("ci_upper should equal sample_mean + z * standard_error.")


def _test_exercise2(env):
    """Check bootstrap_mean output and 95% bootstrap CI percentiles."""
    boot_means = env.get("boot_means")
    boot_ci_lower = env.get("boot_ci_lower")
    boot_ci_upper = env.get("boot_ci_upper")

    if boot_means is None:
        raise AssertionError("Define boot_means by calling bootstrap_mean(sample, reps=5000).")
    if boot_ci_lower is None or boot_ci_upper is None:
        raise AssertionError("Define boot_ci_lower and boot_ci_upper using np.percentile.")

    if len(boot_means) != 5000:
        raise AssertionError("boot_means should have 5000 bootstrap sample means.")

    expected_lower, expected_upper = np.percentile(boot_means, [2.5, 97.5])
    if not np.isclose(boot_ci_lower, expected_lower, atol=1e-5):
        raise AssertionError(
            "boot_ci_lower should be the 2.5th percentile of boot_means. "
            "Use np.percentile(boot_means, [2.5, 97.5])."
        )
    if not np.isclose(boot_ci_upper, expected_upper, atol=1e-5):
        raise AssertionError(
            "boot_ci_upper should be the 97.5th percentile of boot_means. "
            "Use np.percentile(boot_means, [2.5, 97.5])."
        )
    if boot_ci_lower >= boot_ci_upper:
        raise AssertionError("boot_ci_lower should be less than boot_ci_upper.")


def _test_exercise3(env):
    """Check bootstrap CI for the mean drop."""
    ci_drop_lower = env.get("ci_drop_lower")
    ci_drop_upper = env.get("ci_drop_upper")
    boot_drop_means = env.get("boot_drop_means")

    if boot_drop_means is None:
        raise AssertionError("Define boot_drop_means by calling bootstrap_mean(drop, reps=5000).")
    if ci_drop_lower is None or ci_drop_upper is None:
        raise AssertionError("Define ci_drop_lower and ci_drop_upper using np.percentile.")

    expected_lower, expected_upper = np.percentile(boot_drop_means, [2.5, 97.5])
    if not np.isclose(ci_drop_lower, expected_lower, atol=1e-5):
        raise AssertionError(
            "ci_drop_lower should be the 2.5th percentile of boot_drop_means. "
            "Use np.percentile(boot_drop_means, [2.5, 97.5])."
        )
    if not np.isclose(ci_drop_upper, expected_upper, atol=1e-5):
        raise AssertionError(
            "ci_drop_upper should be the 97.5th percentile of boot_drop_means. "
            "Use np.percentile(boot_drop_means, [2.5, 97.5])."
        )
    if ci_drop_lower >= ci_drop_upper:
        raise AssertionError("ci_drop_lower should be less than ci_drop_upper.")
