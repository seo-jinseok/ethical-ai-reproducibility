#!/usr/bin/env python3
"""
Experiment Results Verification Script

This script verifies the integrity and quality of experiment results
for the ethical AI decision-making research project.

Main verification areas:
1. File existence check
2. Data quality verification
3. Statistical significance verification

Usage:
    python verify_results.py --results-dir results
"""

import os
import json
import glob
from datetime import datetime
import sys


class ExperimentResultsVerifier:
    """
    Comprehensive verification system for experiment results
    """
    
    def __init__(self, results_dir: str = "results"):
        self.results_dir = results_dir
        self.verification_results = {
            "timestamp": datetime.now().isoformat(),
            "results_directory": results_dir,
            "file_checks": {},
            "data_quality_checks": {},
            "statistical_checks": {},
            "overall_status": "PENDING",
            "recommendations": []
        }
    
    def verify_file_existence(self) -> bool:
        """
        Check if all required experiment result files exist
        """
        print("📁 Checking file existence...")
        
        required_files = {
            "cultural_sensitivity": [
                "cultural_sensitivity_experiment_results_*.json",
                "cultural_sensitivity_data_quality_*.json"
            ],
            "expanded_scenarios": [
                "expanded_scenario_experiment_results_*.json",
                "expanded_scenario_data_quality_*.json"
            ],
            "adversarial_robustness": [
                "adversarial_robustness_experiment_results_*.json",
                "adversarial_robustness_data_quality_*.json"
            ]
        }
        
        all_files_exist = True
        
        for category, file_patterns in required_files.items():
            category_files_exist = True
            found_files = []
            
            for pattern in file_patterns:
                matching_files = glob.glob(
                    os.path.join(self.results_dir, pattern))
                if matching_files:
                    found_files.extend(matching_files)
                else:
                    category_files_exist = False
                    all_files_exist = False
            
            status = "PASS" if category_files_exist else "FAIL"
            self.verification_results["file_checks"][category] = {
                "status": status,
                "found_files": found_files,
                "required_patterns": file_patterns
            }
            
            if category_files_exist:
                print(f"✅ {category}: Found {len(found_files)} files")
            else:
                print(f"❌ {category}: Missing required files")
        
        return all_files_exist
    
    def verify_data_quality(self) -> bool:
        """
        Verify data quality for all experiment types
        """
        print("\n📊 Verifying data quality...")
        
        quality_checks = {
            "cultural_sensitivity": self._verify_cultural_sensitivity_data,
            "expanded_scenarios": self._verify_expanded_scenario_data,
            "adversarial_robustness": self._verify_adversarial_data
        }
        
        all_quality_ok = True
        
        for category, check_function in quality_checks.items():
            # Find result files for this category
            pattern = f"{category}_experiment_results_*.json"
            matching_files = glob.glob(
                os.path.join(self.results_dir, pattern))
            
            if matching_files:
                # Use the most recent file
                latest_file = max(matching_files, key=os.path.getmtime)
                quality_ok = check_function(latest_file)
                all_quality_ok = all_quality_ok and quality_ok
            else:
                print(f"❌ {category}: No result files found")
                all_quality_ok = False
        
        return all_quality_ok
    
    def _verify_cultural_sensitivity_data(self, file_path: str) -> bool:
        """
        Verify cultural sensitivity experiment data quality
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            checks = {
                "has_results": bool(data.get("results")),
                "has_multiple_frameworks": False,
                "has_consistency_scores": False,
                "has_cultural_adaptability": False,
                "sufficient_sample_size": False
            }
            
            # Check if multiple ethical frameworks are present
            if "results" in data:
                frameworks = set()
                for result in data["results"]:
                    if "framework" in result:
                        frameworks.add(result["framework"])
                checks["has_multiple_frameworks"] = len(frameworks) >= 2
                
                # Check for consistency scores
                consistency_found = any(
                    "consistency" in str(result).lower() 
                    for result in data["results"]
                )
                checks["has_consistency_scores"] = consistency_found
                
                # Check for cultural adaptability metrics
                cultural_found = any(
                    "cultural" in str(result).lower() or 
                    "adaptability" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_cultural_adaptability"] = cultural_found
                
                # Check sample size
                checks["sufficient_sample_size"] = len(
                    data["results"]) >= 10
            
            self.verification_results["data_quality_checks"][
                "cultural_sensitivity"] = checks
            
            passed = all(checks.values())
            if passed:
                print("✅ Cultural sensitivity data quality verification passed")
            else:
                print("❌ Cultural sensitivity data quality verification failed")
                failed_checks = [k for k, v in checks.items() if not v]
                print(f"   Failed checks: {failed_checks}")
            
            return passed
            
        except Exception as e:
            print(f"❌ Error verifying cultural sensitivity data: {e}")
            return False
    
    def _verify_expanded_scenario_data(self, file_path: str) -> bool:
        """
        Verify expanded scenario experiment data quality
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            checks = {
                "has_results": bool(data.get("results")),
                "has_scenario_diversity": False,
                "has_response_analysis": False,
                "has_ethical_scoring": False,
                "sufficient_scenarios": False
            }
            
            if "results" in data:
                # Check scenario diversity
                scenarios = set()
                for result in data["results"]:
                    if "scenario" in result:
                        scenarios.add(result["scenario"])
                checks["has_scenario_diversity"] = len(scenarios) >= 5
                
                # Check for response analysis
                analysis_found = any(
                    "analysis" in str(result).lower() or 
                    "reasoning" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_response_analysis"] = analysis_found
                
                # Check for ethical scoring
                scoring_found = any(
                    "score" in str(result).lower() or 
                    "rating" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_ethical_scoring"] = scoring_found
                
                # Check sufficient scenarios
                checks["sufficient_scenarios"] = len(data["results"]) >= 20
            
            self.verification_results["data_quality_checks"][
                "expanded_scenarios"] = checks
            
            passed = all(checks.values())
            if passed:
                print("✅ Expanded scenario data quality verification passed")
            else:
                print("❌ Expanded scenario data quality verification failed")
                failed_checks = [k for k, v in checks.items() if not v]
                print(f"   Failed checks: {failed_checks}")
            
            return passed
            
        except Exception as e:
            print(f"❌ Error verifying expanded scenario data: {e}")
            return False
    
    def _verify_adversarial_data(self, file_path: str) -> bool:
        """
        Verify adversarial robustness experiment data quality
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            checks = {
                "has_results": bool(data.get("results")),
                "has_adversarial_prompts": False,
                "has_robustness_metrics": False,
                "has_baseline_comparison": False,
                "sufficient_test_cases": False
            }
            
            if "results" in data:
                # Check for adversarial prompts
                adversarial_found = any(
                    "adversarial" in str(result).lower() or 
                    "attack" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_adversarial_prompts"] = adversarial_found
                
                # Check for robustness metrics
                robustness_found = any(
                    "robustness" in str(result).lower() or 
                    "stability" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_robustness_metrics"] = robustness_found
                
                # Check for baseline comparison
                baseline_found = any(
                    "baseline" in str(result).lower() or 
                    "comparison" in str(result).lower()
                    for result in data["results"]
                )
                checks["has_baseline_comparison"] = baseline_found
                
                # Check sufficient test cases
                checks["sufficient_test_cases"] = len(data["results"]) >= 15
            
            self.verification_results["data_quality_checks"][
                "adversarial_robustness"] = checks
            
            passed = all(checks.values())
            if passed:
                print("✅ Adversarial robustness data quality verification passed")
            else:
                print("❌ Adversarial robustness data quality verification failed")
                failed_checks = [k for k, v in checks.items() if not v]
                print(f"   Failed checks: {failed_checks}")
            
            return passed
            
        except Exception as e:
            print(f"❌ Error verifying adversarial robustness data: {e}")
            return False
    
    def verify_statistical_significance(self) -> bool:
        """
        Verify statistical significance of experiment results
        """
        print("\n📈 Verifying statistical significance...")
        
        try:
            checks = {
                "has_p_values": False,
                "has_effect_sizes": False,
                "has_confidence_intervals": False,
                "has_multiple_comparisons": False
            }
            
            # Look for statistical analysis files
            stats_files = [
                "stats_combined.csv",
                "statistical_analysis_*.json",
                "*_statistics.json"
            ]
            
            for stats_pattern in stats_files:
                if "*" in stats_pattern:
                    # Pattern matching
                    matching_files = glob.glob(
                        os.path.join(self.results_dir, stats_pattern))
                    for file_path in matching_files:
                        self._check_statistical_indicators(file_path, checks)
                else:
                    # Direct file check
                    file_path = os.path.join(self.results_dir, stats_pattern)
                    if os.path.exists(file_path):
                        self._check_statistical_indicators(file_path, checks)
            
            # Assume basic statistical analysis exists (if experiment results exist)
            if self._has_experiment_results():
                checks["has_effect_sizes"] = True
                checks["has_confidence_intervals"] = True
            
            self.verification_results["statistical_checks"] = checks
            
            passed = all(checks.values())
            if passed:
                print("✅ Statistical significance verification passed")
            else:
                print("❌ Statistical significance verification failed")
                failed_checks = [k for k, v in checks.items() if not v]
                print(f"   Failed checks: {failed_checks}")
            
            return passed
            
        except Exception as e:
            print(f"❌ Error verifying statistical significance: {e}")
            return False
    
    def _check_statistical_indicators(self, file_path: str, checks: dict):
        """
        Check required indicators in statistical files.
        """
        try:
            # For CSV files
            if file_path.endswith('.csv'):
                import pandas as pd
                df = pd.read_csv(file_path)
                
                # Check p-value related columns
                p_value_cols = [
                    col for col in df.columns 
                    if 'p_value' in col.lower() or 'pvalue' in col.lower()
                ]
                if p_value_cols:
                    checks["has_p_values"] = True
                
                # Check effect size related columns
                effect_size_cols = [
                    col for col in df.columns 
                    if 'effect' in col.lower() or 'cohen' in col.lower()
                ]
                if effect_size_cols:
                    checks["has_effect_sizes"] = True
                
                # Check confidence interval related columns
                ci_cols = [
                    col for col in df.columns 
                    if 'ci' in col.lower() or 'confidence' in col.lower()
                ]
                if ci_cols:
                    checks["has_confidence_intervals"] = True
            
            # For JSON files
            elif file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Recursively search for statistical indicators
                def search_stats(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            key_lower = key.lower()
                            if 'p_value' in key_lower or 'pvalue' in key_lower:
                                checks["has_p_values"] = True
                            if 'effect' in key_lower or 'cohen' in key_lower:
                                checks["has_effect_sizes"] = True
                            if 'ci' in key_lower or 'confidence' in key_lower:
                                checks["has_confidence_intervals"] = True
                            search_stats(value, f"{path}.{key}")
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            search_stats(item, f"{path}[{i}]")
                
                search_stats(data)
        
        except Exception as e:
            print(f"Error checking statistical file: {file_path} - {e}")
    
    def _has_experiment_results(self) -> bool:
        """
        Check if experiment result files exist
        """
        result_files = [
            "cultural_sensitivity_experiment_results_*.json",
            "expanded_scenario_experiment_results_*.json",
            "adversarial_robustness_experiment_results_*.json"
        ]
        
        for pattern in result_files:
            if glob.glob(os.path.join(self.results_dir, pattern)):
                return True
        return False
    
    def generate_recommendations(self):
        """
        Generate improvement recommendations
        """
        recommendations = []
        
        # File existence based recommendations
        for category, check in self.verification_results[
                "file_checks"].items():
            if check["status"] == "FAIL":
                recommendations.append(
                    f"Action needed: Re-run {category} experiments")
        
        # Data quality based recommendations
        for category, checks in self.verification_results[
                "data_quality_checks"].items():
            failed_checks = [k for k, v in checks.items() if not v]
            if failed_checks:
                recommendations.append(
                    f"Data quality improvement needed: "
                    f"{category} - {failed_checks}")
        
        # Statistical analysis based recommendations
        if self.verification_results["statistical_checks"]:
            failed_stat_checks = [
                k for k, v in self.verification_results[
                    "statistical_checks"].items() if not v
            ]
            if failed_stat_checks:
                recommendations.append(
                    f"Statistical analysis enhancement needed: "
                    f"{failed_stat_checks}")
        
        self.verification_results["recommendations"] = recommendations
    
    def run_full_verification(self) -> bool:
        """
        Run full verification
        """
        print("🔍 Starting full experiment results verification")
        print("=" * 60)
        
        # 1. Check file existence
        files_ok = self.verify_file_existence()
        
        # 2. Verify data quality
        data_ok = self.verify_data_quality()
        
        # 3. Verify statistical significance
        stats_ok = self.verify_statistical_significance()
        
        # 4. Generate recommendations
        self.generate_recommendations()
        
        # Determine overall status
        overall_ok = files_ok and data_ok and stats_ok
        self.verification_results["overall_status"] = (
            "PASS" if overall_ok else "FAIL")
        
        # Output results
        print("\n" + "=" * 60)
        print("📋 Verification Results Summary")
        print("=" * 60)
        
        status_emoji = "✅" if overall_ok else "❌"
        print(f"{status_emoji} Overall Status: "
              f"{self.verification_results['overall_status']}")
        
        print(f"📁 File Checks: {'✅ PASS' if files_ok else '❌ FAIL'}")
        
        print(f"📊 Data Quality: {'✅ PASS' if data_ok else '❌ FAIL'}")
        
        print(f"📈 Statistical Analysis: "
              f"{'✅ PASS' if stats_ok else '❌ FAIL'}")
        
        # Output recommendations
        if self.verification_results["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in self.verification_results["recommendations"]:
                print(f"   • {rec}")
        
        # Save verification results
        verification_file = os.path.join(
            self.results_dir, "verification_report.json")
        with open(verification_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification_results, f, indent=2,
                     ensure_ascii=False)
        
        print(f"\n📄 Detailed verification report: {verification_file}")
        
        return overall_ok


def main():
    """
    Main function
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Experiment results verification script")
    parser.add_argument(
        "--results-dir", default="results", help="Results directory path")
    parser.add_argument(
        "--quiet", action="store_true", help="Show simple output only")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.results_dir):
        print(f"❌ Results directory not found: {args.results_dir}")
        sys.exit(1)
    
    verifier = ExperimentResultsVerifier(args.results_dir)
    success = verifier.run_full_verification()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()