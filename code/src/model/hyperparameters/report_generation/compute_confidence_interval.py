from typing import Tuple

import numpy as np
from numba import jit


@jit(nopython=True, cache=True, fastmath=True)
def compute_confidence_interval(
    rewards: np.ndarray, confidence_level: float, confidence_iterations: int
) -> Tuple[float, float, float]:
    """Compute the confidence interval from a series of samples.

    This method uses bootstrapping to reduce sensitivity to outliers.

    Args:
        rewards (np.ndarray): Array of samples.
        confidence_level (float): Desired confidence level (e.g., 0.95 for 95%
            confidence interval).
        confidence_iterations (int): Number of bootstrap iterations.

    Returns:
        Tuple: the confidence interval, the lower bound
            mean and upper bound.
    """
    sample_count = len(rewards)
    means = np.empty(confidence_iterations)

    for index in range(confidence_iterations):
        # Bootstrap sampling
        resample_indices = np.random.randint(0, sample_count, sample_count)
        resample = rewards[resample_indices]

        means[index] = np.mean(resample)

    # Calculate confidence interval using percentiles
    lower_percentile = (1 - confidence_level) / 2 * 100
    upper_percentile = 100 - lower_percentile

    lower_bound = np.percentile(means, lower_percentile)
    upper_bound = np.percentile(means, upper_percentile)

    return float(lower_bound), float(np.mean(rewards)), float(upper_bound)
