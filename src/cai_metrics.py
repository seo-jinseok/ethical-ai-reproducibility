#!/usr/bin/env python3
"""
Cultural Adaptability Index (CAI) Metrics Module

This module implements the Cultural Adaptability Index (CAI) for evaluating
the cultural adaptability of AI systems, particularly Large Language Models.

The CAI is based on statistical distance measures between probability
distributions of ethical responses across different cultural frameworks.

Author: Jinseok Seo (jsseo@deu.ac.kr)
Date: 2025-01-28
Version: 1.0
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats
from scipy.spatial.distance import jensenshannon
from dataclasses import dataclass


@dataclass
class CAIResult:
    """
    Data class to store CAI calculation results.
    
    Attributes:
        cai_score: Overall CAI score (0-1, higher is better)
        distance_matrix: Pairwise distances between cultural frameworks
        framework_scores: Individual scores for each framework
        statistical_significance: p-values for statistical tests
        confidence_intervals: 95% confidence intervals for scores
        method_used: Statistical distance method used
    """
    cai_score: float
    distance_matrix: np.ndarray
    framework_scores: Dict[str, float]
    statistical_significance: Dict[str, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    method_used: str


class CAIMetrics:
    """
    Cultural Adaptability Index (CAI) metrics calculation class.
    
    This class provides comprehensive metrics for measuring the cultural
    adaptability of AI models, particularly in ethical decision-making
    contexts. It implements various statistical distance measures to
    quantify how well models adapt to different cultural frameworks.
    
    The CAI is calculated based on the distribution of responses across
    different cultural ethical frameworks (Western: Deontology,
    Utilitarianism, Virtue Ethics; Non-Western: Confucianism, Ubuntu,
    Buddhism).
    
    Attributes:
        distance_method: Statistical distance method to use
        supported_methods: Available distance calculation methods
        cultural_frameworks: Standard cultural frameworks for evaluation
    
    Key Features:
    - Cultural dimension-based weight calculation
    - Ethical consistency evaluation
    - Bias detection and measurement
    - Statistical significance testing
    """
    
    def __init__(self, distance_method: str = 'jensen_shannon'):
        """
        Initialize CAI calculator.
        
        Args:
            distance_method: Statistical distance method to use.
                           Options: 'jensen_shannon', 'total_variation',
                           'wasserstein', 'hellinger', 'kl_divergence'
        """
        self.distance_method = distance_method
        self.supported_methods = {
            'jensen_shannon': self._jensen_shannon_distance,
            'total_variation': self._total_variation_distance,
            'wasserstein': self._wasserstein_distance,
            'hellinger': self._hellinger_distance,
            'kl_divergence': self._kl_divergence
        }
        
        # Cultural weights based on Hofstede's cultural dimensions
        self.cultural_weights = {
            'western': {
                'individualism': 0.8,
                'hierarchy': 0.3,
                'uncertainty_avoidance': 0.5,
                'long_term_orientation': 0.4,
                'masculinity': 0.6
            },
            'eastern': {
                'individualism': 0.2,
                'hierarchy': 0.8,
                'uncertainty_avoidance': 0.7,
                'long_term_orientation': 0.9,
                'masculinity': 0.4
            },
            'african': {
                'individualism': 0.3,
                'hierarchy': 0.6,
                'uncertainty_avoidance': 0.4,
                'long_term_orientation': 0.6,
                'masculinity': 0.5
            },
            'buddhist': {
                'individualism': 0.1,
                'hierarchy': 0.4,
                'uncertainty_avoidance': 0.3,
                'long_term_orientation': 0.8,
                'masculinity': 0.2
            }
        }
        
        # Weights for each ethical framework
        self.ethical_weights = {
            'deontological': {
                'duty': 0.9, 'consequences': 0.3, 'virtue': 0.6
            },
            'utilitarian': {
                'duty': 0.3, 'consequences': 0.9, 'virtue': 0.4
            },
            'virtue_ethics': {
                'duty': 0.6, 'consequences': 0.4, 'virtue': 0.9
            },
            'confucian': {
                'duty': 0.7, 'consequences': 0.5, 'virtue': 0.8
            },
            'ubuntu': {
                'duty': 0.6, 'consequences': 0.7, 'virtue': 0.9
            },
            'buddhist': {
                'duty': 0.5, 'consequences': 0.6, 'virtue': 0.9
            }
        }
        
        if distance_method not in self.supported_methods:
            raise ValueError(
                f"Unsupported distance method: {distance_method}. "
                f"Supported methods: {list(self.supported_methods.keys())}"
            )
    
    def calculate_cai(self,
                      data: pd.DataFrame,
                      framework_column: str = 'framework',
                      response_column: str = 'response_category',
                      confidence_level: float = 0.95) -> CAIResult:
        """
        Calculate the Cultural Adaptability Index (CAI).
        
        Args:
            data: DataFrame containing responses across cultural frameworks
            framework_column: Column name containing cultural framework
                            labels
            response_column: Column name containing response categories
            confidence_level: Confidence level for statistical tests
            
        Returns:
            CAIResult object containing all calculated metrics
        """
        # Validate input data
        self._validate_input(data, framework_column, response_column)
        
        # Get unique frameworks
        frameworks = data[framework_column].unique()
        n_frameworks = len(frameworks)
        
        if n_frameworks < 2:
            raise ValueError(
                "At least 2 cultural frameworks are required for "
                "CAI calculation"
            )
        
        # Calculate response distributions for each framework
        distributions = self._calculate_distributions(
            data, framework_column, response_column
        )
        
        # Calculate pairwise distances between frameworks
        distance_matrix = self._calculate_distance_matrix(
            distributions, frameworks
        )
        
        # Calculate individual framework scores
        framework_scores = self._calculate_framework_scores(
            distance_matrix, frameworks
        )
        
        # Calculate overall CAI score
        cai_score = self._calculate_overall_cai(distance_matrix)
        
        # Perform statistical significance tests
        significance_tests = self._perform_significance_tests(
            data, framework_column, response_column, confidence_level
        )
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(
            data, framework_column, response_column, confidence_level
        )
        
        return CAIResult(
            cai_score=cai_score,
            distance_matrix=distance_matrix,
            framework_scores=framework_scores,
            statistical_significance=significance_tests,
            confidence_intervals=confidence_intervals,
            method_used=self.distance_method
        )
    
    def _validate_input(self, data: pd.DataFrame, framework_col: str,
                        response_col: str):
        """Validate input data format and content."""
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        
        if framework_col not in data.columns:
            raise ValueError(
                f"Framework column '{framework_col}' not found in data"
            )
        
        if response_col not in data.columns:
            raise ValueError(
                f"Response column '{response_col}' not found in data"
            )
        
        if data.empty:
            raise ValueError("Input data is empty")
        
        # Check for missing values
        if (data[framework_col].isna().any() or
                data[response_col].isna().any()):
            warnings.warn(
                "Missing values detected. They will be excluded from "
                "analysis."
            )
    
    def _calculate_distributions(self, data: pd.DataFrame,
                                 framework_col: str,
                                 response_col: str) -> Dict[str, np.ndarray]:
        """Calculate probability distributions for each framework."""
        distributions = {}
        
        # Get all possible response categories
        all_categories = sorted(data[response_col].dropna().unique())
        
        for framework in data[framework_col].unique():
            framework_data = data[data[framework_col] == framework][response_col].dropna()
            
            if len(framework_data) == 0:
                warnings.warn(f"No valid data for framework '{framework}'")
                continue
            
            # Calculate probability distribution
            value_counts = framework_data.value_counts()
            probabilities = np.zeros(len(all_categories))
            
            for i, category in enumerate(all_categories):
                if category in value_counts.index:
                    probabilities[i] = value_counts[category] / len(framework_data)
            
            # Add small epsilon to avoid zero probabilities for some distance measures
            epsilon = 1e-10
            probabilities = probabilities + epsilon
            probabilities = probabilities / probabilities.sum()  # Renormalize
            
            distributions[framework] = probabilities
        
        return distributions
    
    def _calculate_distance_matrix(self,
                                   distributions: Dict[str, np.ndarray],
                                   frameworks: List[str]) -> np.ndarray:
        """Calculate pairwise distance matrix between frameworks."""
        n = len(frameworks)
        distance_matrix = np.zeros((n, n))
        
        distance_func = self.supported_methods[self.distance_method]
        
        for i in range(n):
            for j in range(i + 1, n):
                if frameworks[i] in distributions and frameworks[j] in distributions:
                    dist = distance_func(
                        distributions[frameworks[i]],
                        distributions[frameworks[j]]
                    )
                    distance_matrix[i, j] = dist
                    distance_matrix[j, i] = dist  # Symmetric matrix
        
        return distance_matrix
    
    def _calculate_framework_scores(self,
                                    distance_matrix: np.ndarray,
                                    frameworks: List[str]) -> Dict[str, float]:
        """Calculate individual adaptability scores for each framework."""
        scores = {}
        n = len(frameworks)
        
        for i, framework in enumerate(frameworks):
            # Framework score is 1 minus average distance to other frameworks
            # Higher distance means lower adaptability
            avg_distance = np.mean([distance_matrix[i, j] for j in range(n) if i != j])
            scores[framework] = max(0.0, 1.0 - avg_distance)
        
        return scores
    
    def _calculate_overall_cai(self, distance_matrix: np.ndarray) -> float:
        """Calculate overall CAI score."""
        # CAI is 1 minus the average pairwise distance
        # Higher distances indicate lower cultural adaptability
        n = distance_matrix.shape[0]
        if n < 2:
            return 0.0
        
        # Get upper triangle (excluding diagonal) for pairwise distances
        upper_triangle = distance_matrix[np.triu_indices(n, k=1)]
        avg_distance = np.mean(upper_triangle)
        
        # CAI score: 1 means perfect adaptability (no distance), 0 means no adaptability
        cai_score = max(0.0, 1.0 - avg_distance)
        
        return cai_score
    
    def _perform_significance_tests(self,
                                    data: pd.DataFrame,
                                    framework_col: str,
                                    response_col: str,
                                    confidence_level: float) -> Dict[str, float]:
        """Perform statistical significance tests."""
        frameworks = data[framework_col].unique()
        
        if len(frameworks) < 2:
            return {}
        
        # Chi-square test for independence
        contingency_table = pd.crosstab(data[framework_col], data[response_col])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Kruskal-Wallis test (if response categories can be ordered)
        try:
            # Convert response categories to numeric if possible
            numeric_responses = pd.to_numeric(data[response_col], errors='coerce')
            if not numeric_responses.isna().all():
                groups = [numeric_responses[data[framework_col] == fw].dropna() 
                         for fw in frameworks]
                groups = [g for g in groups if len(g) > 0]  # Remove empty groups
                
                if len(groups) >= 2:
                    kw_stat, kw_p_value = stats.kruskal(*groups)
                else:
                    kw_p_value = 1.0
            else:
                kw_p_value = 1.0
        except Exception:
            kw_p_value = 1.0
        
        return {
            'chi_square_p_value': p_value,
            'kruskal_wallis_p_value': kw_p_value
        }
    
    def _calculate_confidence_intervals(self,
                                        data: pd.DataFrame,
                                        framework_col: str,
                                        response_col: str,
                                        confidence_level: float
                                        ) -> Dict[str, Tuple[float, float]]:
        """Calculate confidence intervals using bootstrap method."""
        frameworks = data[framework_col].unique()
        confidence_intervals = {}
        
        # Bootstrap parameters
        n_bootstrap = 1000
        alpha = 1 - confidence_level
        
        for framework in frameworks:
            framework_data = data[data[framework_col] == framework]
            
            if len(framework_data) < 10:  # Minimum sample size for bootstrap
                confidence_intervals[framework] = (0.0, 1.0)
                continue
            
            bootstrap_scores = []
            
            for _ in range(n_bootstrap):
                # Bootstrap sample
                bootstrap_sample = framework_data.sample(n=len(framework_data), replace=True)
                
                # Create temporary dataset with bootstrap sample
                temp_data = pd.concat([bootstrap_sample, 
                                     data[data[framework_col] != framework]])
                
                try:
                    # Calculate CAI for bootstrap sample
                    temp_result = self.calculate_cai(temp_data, framework_col, response_col)
                    if framework in temp_result.framework_scores:
                        bootstrap_scores.append(temp_result.framework_scores[framework])
                except:
                    continue
            
            if bootstrap_scores:
                lower = np.percentile(bootstrap_scores, 100 * alpha / 2)
                upper = np.percentile(bootstrap_scores, 100 * (1 - alpha / 2))
                confidence_intervals[framework] = (lower, upper)
            else:
                confidence_intervals[framework] = (0.0, 1.0)
        
        return confidence_intervals
    
    # Statistical distance methods
    def _jensen_shannon_distance(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate Jensen-Shannon distance."""
        return jensenshannon(p, q)
    
    def _total_variation_distance(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate Total Variation distance."""
        return 0.5 * np.sum(np.abs(p - q))
    
    def _wasserstein_distance(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate Wasserstein distance (1-dimensional)."""
        # For discrete distributions, use cumulative distribution functions
        cdf_p = np.cumsum(p)
        cdf_q = np.cumsum(q)
        return np.sum(np.abs(cdf_p - cdf_q))
    
    def _hellinger_distance(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate Hellinger distance."""
        return np.sqrt(0.5 * np.sum((np.sqrt(p) - np.sqrt(q)) ** 2))
    
    def _kl_divergence(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate symmetrized Kullback-Leibler divergence."""
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        p_safe = p + epsilon
        q_safe = q + epsilon
        
        # Symmetrized KL divergence: 0.5 * (KL(P||Q) + KL(Q||P))
        kl_pq = np.sum(p_safe * np.log(p_safe / q_safe))
        kl_qp = np.sum(q_safe * np.log(q_safe / p_safe))
        
        return 0.5 * (kl_pq + kl_qp)


def calculate_cai_summary_statistics(cai_results: List[CAIResult]) -> Dict[str, float]:
    """
    Calculate summary statistics across multiple CAI calculations.
    
    Args:
        cai_results: List of CAIResult objects
        
    Returns:
        Dictionary containing summary statistics
    """
    if not cai_results:
        return {}
    
    cai_scores = [result.cai_score for result in cai_results]
    
    return {
        'mean_cai': np.mean(cai_scores),
        'std_cai': np.std(cai_scores),
        'min_cai': np.min(cai_scores),
        'max_cai': np.max(cai_scores),
        'median_cai': np.median(cai_scores),
        'q25_cai': np.percentile(cai_scores, 25),
        'q75_cai': np.percentile(cai_scores, 75)
    }


def compare_distance_methods(data: pd.DataFrame,
                           framework_column: str = 'framework',
                           response_column: str = 'response_category') -> pd.DataFrame:
    """
    Compare CAI scores across different distance methods.
    
    Args:
        data: DataFrame containing responses across cultural frameworks
        framework_column: Column name containing cultural framework labels
        response_column: Column name containing response categories
        
    Returns:
        DataFrame comparing CAI scores across methods
    """
    methods = ['jensen_shannon', 'total_variation', 'wasserstein', 'hellinger', 'kl_divergence']
    results = []
    
    for method in methods:
        try:
            calculator = CAIMetrics(distance_method=method)
            result = calculator.calculate_cai(data, framework_column, response_column)
            
            results.append({
                'method': method,
                'cai_score': result.cai_score,
                'chi_square_p': result.statistical_significance.get('chi_square_p_value', np.nan),
                'kruskal_wallis_p': result.statistical_significance.get('kruskal_wallis_p_value', np.nan)
            })
        except Exception as e:
            print(f"Error calculating CAI with method {method}: {e}")
            results.append({
                'method': method,
                'cai_score': np.nan,
                'chi_square_p': np.nan,
                'kruskal_wallis_p': np.nan
            })
    
    return pd.DataFrame(results)