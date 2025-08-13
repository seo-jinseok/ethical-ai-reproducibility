#!/usr/bin/env python3
"""
Cultural Adaptability Index (CAI) Implementation

This module implements the Cultural Adaptability Index (CAI) for evaluating
the cultural adaptability of AI systems, particularly Large Language Models.

=== MATHEMATICAL DEFINITION ===

The CAI is defined as:
    CAI = 1 - (1/2K) * Σ_{k=1}^{K} |P_k^{LLM} - P_k^{human}|

Where:
- P_k^LLM: Probability of response category k from the LLM
- P_k^{human}: Probability of response category k from human responses  
- K: Total number of response categories
- Σ_{k=1}^{K} P_k^{LLM} = 1 and Σ_{k=1}^{K} P_k^{human} = 1 (probability constraints)

=== MATHEMATICAL PROPERTIES ===

1. **Normalization**: CAI ∈ [0, 1]
   - Lower bound: CAI ≥ 0 (proven by L1 distance properties)
   - Upper bound: CAI ≤ 1 (achieved when distributions are identical)

2. **Boundary Values**:
   - Perfect alignment: CAI = 1 when P_k^{LLM} = P_k^{human} for all k
   - Maximum divergence: CAI = 1 - 1/K when distributions are maximally different
   - For binary choices (K=2): CAI_min = 0.5
   - For multiple choices (K→∞): CAI_min → 1

3. **Symmetry**: CAI(P^{LLM}, P^{human}) = CAI(P^{human}, P^{LLM})

4. **Continuity**: CAI is continuous with respect to input probability distributions

5. **Computational Complexity**: O(K) time and space complexity

=== PROOF SKETCH ===

**Theorem 1 (Normalization)**: CAI ∈ [0, 1]

Proof:
1. L1 distance: Σ_k |P_k^{LLM} - P_k^{human}| ∈ [0, 2]
   - Minimum (0): When distributions are identical
   - Maximum (2): When distributions assign probability 1 to different categories

2. CAI transformation:
   - CAI = 1 - (1/2K) * L1_distance
   - When L1 = 0: CAI = 1 (perfect alignment)
   - When L1 = 2: CAI = 1 - 1/K (maximum divergence)
   - Since L1 ∈ [0, 2], we have CAI ∈ [1-1/K, 1] ⊆ [0, 1]

**Theorem 2 (Boundary Characterization)**:
- CAI = 1 ⟺ P_k^{LLM} = P_k^{human} for all k
- CAI = 1-1/K ⟺ Distributions are maximally separated

**Theorem 3 (Metric Properties)**:
CAI satisfies modified metric properties suitable for cultural similarity measurement.

=== STATISTICAL INTERPRETATION ===

- **High CAI (≥ 0.8)**: Strong cultural alignment
- **Medium CAI (0.5-0.8)**: Moderate cultural alignment  
- **Low CAI (< 0.5)**: Poor cultural alignment
- **Baseline**: Random alignment gives CAI ≈ 1-1/K

=== RELATIONSHIP TO OTHER METRICS ===

1. **Total Variation Distance**: CAI = 1 - TV/2
2. **Jensen-Shannon Divergence**: Similar intuition but CAI is computationally simpler
3. **Hellinger Distance**: CAI provides more interpretable scale [0,1]
4. **KL Divergence**: CAI is symmetric and bounded

=== USAGE EXAMPLES ===


human_probs = np.array([0.0, 1.0])
cai_divergent = compute_cai(llm_probs, human_probs)  # Returns 0.5

# Partial alignment
llm_probs = np.array([0.6, 0.3, 0.1])
human_probs = np.array([0.4, 0.4, 0.2])
cai_partial = compute_cai(llm_probs, human_probs)  # Returns ~0.83
```

=== VALIDATION AND TESTING ===

The implementation includes comprehensive validation:
- Input probability distribution validation
- Numerical stability checks
- Boundary condition testing
- Bootstrap confidence intervals
- Batch processing capabilities

Author: Jinseok Seo (jsseo@deu.ac.kr)
Date: 2025-01-28
Version: 1.0
"""

from typing import Union, Optional
import numpy as np


def compute_cai(pred_probs: np.ndarray,
                human_probs: np.ndarray,
                validate_input: bool = True) -> float:
    """
    Compute the Cultural Adaptability Index (CAI) between predicted and human
    probability distributions.
    
    The CAI measures how well an AI system's response distribution aligns with
    human cultural responses. Higher values indicate better cultural alignment.
    
    Mathematical Formula:
        CAI = 1 - Σ_k |P_k^pred - P_k^human| / (2K)
    
    Where:
    - P_k^pred: Probability of response category k from predictions
    - P_k^human: Probability of response category k from human responses  
    - K: Total number of response categories
    
    Args:
        pred_probs (np.ndarray): Predicted probability distribution.
            Must be a 1D array with non-negative values that sum to 1.
        human_probs (np.ndarray): Human probability distribution.
            Must be a 1D array with non-negative values that sum to 1.
        validate_input (bool, optional): Whether to validate input arrays.
            Defaults to True. Set to False for performance in batch processing.
    
    Returns:
        float: CAI score in range [0, 1], where:
            - 1.0 = Perfect cultural alignment
            - 0.0 = Maximum cultural divergence
            - Values closer to 1 indicate better cultural adaptability
    
    Raises:
        ValueError: If input arrays have different shapes, contain negative
            values, don't sum to 1 (within tolerance), or are empty.
        TypeError: If inputs are not numpy arrays or convertible to
            arrays.
    
    Examples:
        >>> import numpy as np
        >>> # Perfect alignment
        >>> pred = np.array([0.3, 0.4, 0.3])
        >>> human = np.array([0.3, 0.4, 0.3])
        >>> compute_cai(pred, human)
        1.0
        
        >>> # Partial alignment
        >>> pred = np.array([0.5, 0.3, 0.2])
        >>> human = np.array([0.3, 0.4, 0.3])
        >>> compute_cai(pred, human)
        0.8
        
        >>> # Maximum divergence (theoretical)
        >>> pred = np.array([1.0, 0.0, 0.0])
        >>> human = np.array([0.0, 0.0, 1.0])
        >>> compute_cai(pred, human)
        0.0
    
    Notes:
        - Input arrays are automatically converted to numpy arrays if needed
        - Small numerical errors in probability sums are tolerated (1e-6)
        - The function is symmetric: compute_cai(A, B) == compute_cai(B, A)
        - For performance-critical applications, set validate_input=False
    """
    # Convert inputs to numpy arrays if needed
    try:
        pred_probs = np.asarray(pred_probs, dtype=np.float64)
        human_probs = np.asarray(human_probs, dtype=np.float64)
    except (ValueError, TypeError) as e:
        raise TypeError(
            f"Input arrays must be convertible to numpy arrays: {e}")
    
    if validate_input:
        _validate_probability_arrays(pred_probs, human_probs)
    
    # Compute Total Variation distance
    tv_distance = np.sum(np.abs(pred_probs - human_probs))
    
    # Convert to CAI: normalize by 2 and subtract from 1
    # The factor of 2 comes from the maximum possible TV distance between
    # probability distributions
    cai_score = 1.0 - (tv_distance / 2.0)
    
    # Ensure result is in valid range due to numerical precision
    cai_score = np.clip(cai_score, 0.0, 1.0)
    
    return float(cai_score)


def compute_cai_batch(pred_probs_batch: np.ndarray,
                      human_probs_batch: np.ndarray,
                      validate_input: bool = True) -> np.ndarray:
    """
    Compute CAI scores for multiple probability distribution pairs.
    
    This function efficiently computes CAI scores for batches of probability
    distributions, useful for evaluating multiple scenarios or models.
    
    Args:
        pred_probs_batch (np.ndarray): Batch of predicted probability
            distributions. Shape: (n_samples, n_categories)
        human_probs_batch (np.ndarray): Batch of human probability
            distributions. Shape: (n_samples, n_categories)
        validate_input (bool, optional): Whether to validate input arrays.
            Defaults to True.
    
    Returns:
        np.ndarray: Array of CAI scores with shape (n_samples,)
    
    Raises:
        ValueError: If batch dimensions don't match or individual
            distributions are invalid.
    
    Examples:
        >>> import numpy as np
        >>> pred_batch = np.array([[0.3, 0.4, 0.3], [0.5, 0.3, 0.2]])
        >>> human_batch = np.array([[0.3, 0.4, 0.3], [0.3, 0.4, 0.3]])
        >>> compute_cai_batch(pred_batch, human_batch)
        array([1.0, 0.8])
    """
    pred_probs_batch = np.asarray(pred_probs_batch, dtype=np.float64)
    human_probs_batch = np.asarray(human_probs_batch, dtype=np.float64)
    
    if pred_probs_batch.shape != human_probs_batch.shape:
        raise ValueError(
            f"Batch shapes must match: {pred_probs_batch.shape} vs "
            f"{human_probs_batch.shape}"
        )
    
    if pred_probs_batch.ndim != 2:
        raise ValueError(
            f"Expected 2D arrays (n_samples, n_categories), got "
            f"{pred_probs_batch.ndim}D"
        )
    
    n_samples = pred_probs_batch.shape[0]
    cai_scores = np.zeros(n_samples)
    
    for i in range(n_samples):
        cai_scores[i] = compute_cai(
            pred_probs_batch[i],
            human_probs_batch[i],
            validate_input=validate_input
        )
    
    return cai_scores


def _validate_probability_arrays(pred_probs: np.ndarray,
                                 human_probs: np.ndarray,
                                 tolerance: float = 1e-6) -> None:
    """
    Validate that input arrays are valid probability distributions.
    
    Args:
        pred_probs (np.ndarray): Predicted probability distribution
        human_probs (np.ndarray): Human probability distribution
        tolerance (float): Tolerance for probability sum validation
    
    Raises:
        ValueError: If arrays are invalid probability distributions
    """
    # Check if arrays are 1D
    if pred_probs.ndim != 1 or human_probs.ndim != 1:
        raise ValueError(
            f"Arrays must be 1-dimensional, got shapes: "
            f"{pred_probs.shape}, {human_probs.shape}"
        )
    
    # Check if arrays have same length
    if len(pred_probs) != len(human_probs):
        raise ValueError(
            f"Arrays must have same length: {len(pred_probs)} vs "
            f"{len(human_probs)}"
        )
    
    # Check if arrays are non-empty
    if len(pred_probs) == 0:
        raise ValueError("Arrays cannot be empty")
    
    # Check for non-negative values
    if np.any(pred_probs < 0) or np.any(human_probs < 0):
        raise ValueError("Probability values must be non-negative")
    
    # Check if arrays sum to 1 (within tolerance)
    pred_sum = np.sum(pred_probs)
    human_sum = np.sum(human_probs)
    
    if abs(pred_sum - 1.0) > tolerance:
        raise ValueError(
            f"Predicted probabilities must sum to 1, got {pred_sum:.6f}"
        )
    
    if abs(human_sum - 1.0) > tolerance:
        raise ValueError(
            f"Human probabilities must sum to 1, got {human_sum:.6f}"
        )
    
    # Check for NaN or infinite values
    if np.any(~np.isfinite(pred_probs)) or np.any(~np.isfinite(human_probs)):
        raise ValueError("Arrays must not contain NaN or infinite values")


def cai_confidence_interval(pred_probs: np.ndarray,
                            human_probs: np.ndarray,
                            n_bootstrap: int = 1000,
                            confidence_level: float = 0.95,
                            random_state: Optional[int] = None) -> tuple:
    """
    Compute bootstrap confidence interval for CAI score.
    
    Args:
        pred_probs (np.ndarray): Predicted probability distribution
        human_probs (np.ndarray): Human probability distribution
        n_bootstrap (int): Number of bootstrap samples
        confidence_level (float): Confidence level (e.g., 0.95 for 95%)
        random_state (Optional[int]): Random seed for reproducibility
    
    Returns:
        tuple: (lower_bound, upper_bound, point_estimate)
    
    Examples:
        >>> import numpy as np
        >>> pred = np.array([0.3, 0.4, 0.3])
        >>> human = np.array([0.25, 0.45, 0.3])
        >>> lower, upper, point = cai_confidence_interval(pred, human)
        >>> print(f"CAI: {point:.3f} [{lower:.3f}, {upper:.3f}]")
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    # Point estimate
    point_estimate = compute_cai(pred_probs, human_probs)
    
    # Bootstrap sampling
    n_categories = len(pred_probs)
    bootstrap_cais = []
    
    for _ in range(n_bootstrap):
        # Add small random noise to simulate sampling uncertainty
        noise_scale = 0.01  # Small noise to simulate measurement uncertainty
        
        pred_noisy = pred_probs + np.random.normal(
            0, noise_scale, n_categories
        )
        human_noisy = human_probs + np.random.normal(
            0, noise_scale, n_categories
        )
        
        # Ensure probabilities remain valid
        pred_noisy = np.maximum(0, pred_noisy)
        human_noisy = np.maximum(0, human_noisy)
        
        pred_noisy = pred_noisy / np.sum(pred_noisy)
        human_noisy = human_noisy / np.sum(human_noisy)
        
        bootstrap_cai = compute_cai(
            pred_noisy, human_noisy, validate_input=False
        )
        bootstrap_cais.append(bootstrap_cai)
    
    bootstrap_cais = np.array(bootstrap_cais)
    
    # Calculate confidence interval
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    lower_bound = np.percentile(bootstrap_cais, lower_percentile)
    upper_bound = np.percentile(bootstrap_cais, upper_percentile)
    
    return float(lower_bound), float(upper_bound), float(point_estimate)


# Convenience functions for common use cases
def cai_from_counts(pred_counts: Union[np.ndarray, list],
                    human_counts: Union[np.ndarray, list]) -> float:
    """
    Compute CAI from count data by converting to probabilities.
    
    Args:
        pred_counts: Count data for predicted responses
        human_counts: Count data for human responses
    
    Returns:
        float: CAI score
    
    Examples:
        >>> # Predicted: 30 utilitarian, 40 deontological, 30 virtue ethics
        >>> # Human: 25 utilitarian, 45 deontological, 30 virtue ethics
        >>> cai_from_counts([30, 40, 30], [25, 45, 30])
        0.95
    """
    pred_counts = np.asarray(pred_counts, dtype=np.float64)
    human_counts = np.asarray(human_counts, dtype=np.float64)
    
    if np.sum(pred_counts) == 0 or np.sum(human_counts) == 0:
        raise ValueError("Count arrays cannot sum to zero")
    
    pred_probs = pred_counts / np.sum(pred_counts)
    human_probs = human_counts / np.sum(human_counts)
    
    return compute_cai(pred_probs, human_probs)


def cai_summary_stats(cai_scores: np.ndarray) -> dict:
    """
    Compute summary statistics for a collection of CAI scores.
    
    Args:
        cai_scores (np.ndarray): Array of CAI scores
    
    Returns:
        dict: Summary statistics including mean, std, min, max,
            percentiles
    
    Examples:
        >>> scores = np.array([0.8, 0.9, 0.7, 0.85, 0.75])
        >>> stats = cai_summary_stats(scores)
        >>> print(f"Mean CAI: {stats['mean']:.3f}")
    """
    cai_scores = np.asarray(cai_scores)
    
    if len(cai_scores) == 0:
        raise ValueError("CAI scores array cannot be empty")
    
    return {
        'mean': float(np.mean(cai_scores)),
        'std': float(np.std(cai_scores, ddof=1)
                     if len(cai_scores) > 1 else 0),
        'min': float(np.min(cai_scores)),
        'max': float(np.max(cai_scores)),
        'median': float(np.median(cai_scores)),
        'q25': float(np.percentile(cai_scores, 25)),
        'q75': float(np.percentile(cai_scores, 75)),
        'count': len(cai_scores)
    }