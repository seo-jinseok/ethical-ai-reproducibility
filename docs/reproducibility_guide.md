# Reproducibility Package

## Overview

This reproducibility package provides the necessary code, data, and environment configuration information to reproduce all experiments of the "LLM Ethical Decision-Making Evaluation Framework".

## Package Structure

```
AgentLaboratory/
├── research_dir/
│   ├── src/                           # Core implementation code
│   ├── data/                          # Experimental datasets
│   ├── results/                       # Experimental results
│   ├── docs/                          # Documentation
│   └── requirements.txt               # Python dependencies
├── models/                            # Pre-trained models
└── README.md                          # Project overview
```

## Core Implementation Files

### 1. Ethical Evaluation System
- `enhanced_ethical_evaluator.py`: Integrated ethical evaluation framework
- `cultural_bias_detector.py`: Cultural bias detection system
- `enhanced_cultural_bias_system.py`: Enhanced cultural bias analysis

### 2. Experiment Execution Scripts
- `run_cultural_sensitivity_experiments.py`: Cultural sensitivity experiments
- `run_expanded_scenario_experiments.py`: Extended scenario experiments
- `adversarial_testing_system.py`: Adversarial robustness testing

### 3. Analysis and Visualization
- `statistical_analysis_framework.py`: Statistical analysis framework
- `analyze_cultural_sensitivity_results.py`: Cultural sensitivity results analysis
- `analyze_framework_performance.py`: Framework performance analysis

### 4. Expert Panel Evaluation
- `expert_panel_integration.py`: Expert panel integration system
- `expert_panel_evaluator.py`: Expert evaluation tools

## Environment Setup

### 1. System Requirements
- Python 3.8+
- Minimum 8GB RAM (Recommended: 16GB)
- 10GB+ storage space
- macOS, Linux, or Windows

### 2. Ollama Installation and Setup
```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama service
ollama serve

# Download required models
ollama pull llama3.2:3b
ollama pull gemma2:2b
ollama pull mistral:7b
ollama pull qwen2.5:7b
```

### 3. Python Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
cd research_dir
pip install -r requirements.txt
```

## Datasets

### 1. Ethical Scenario Data
- `data/ethical_scenarios.csv`: Basic ethical dilemma scenarios
- `data/moral_dataset.csv`: Moral judgment dataset

### 2. Expert Panel Data
- `expert_panel_data.csv`: Expert evaluation results
- `expert_panel_config.json`: Expert panel configuration

### 3. Experimental Results Data
- `results/cultural_sensitivity_experiment_results_*.json`
- `results/expanded_scenario_results_*.json`
- `results/adversarial_robustness_analysis_report_*.json`

## Experiment Reproduction Guide

### 1. Full Experimental Pipeline Execution
```bash
cd research_dir/src

# Phase 1: Cultural sensitivity experiments
python run_cultural_sensitivity_experiments.py

# Phase 2: Extended scenario experiments
python run_expanded_scenario_experiments.py

# Phase 3: Adversarial robustness testing
python adversarial_testing_system.py

# Phase 4: Results analysis
python analyze_cultural_sensitivity_results.py
python analyze_framework_performance.py
```

### 2. Individual Experiment Execution
```bash
# Cultural sensitivity testing with specific model
python run_cultural_sensitivity_experiments.py --model llama3.2:3b --cultural_orientation individualistic

# Specific ethical framework testing
python run_expanded_scenario_experiments.py --framework deontological --scenario_type privacy
```

### 3. Statistical Analysis Execution
```bash
# Statistical analysis framework testing
python statistical_framework_demo.py

# Effect size and power analysis
python test_statistical_framework.py
```

## Result Verification

### 1. Automated Verification Scripts
```python
# Check existence of result files
python -c "
import os
result_files = [
    'results/cultural_sensitivity_experiment_results_*.json',
    'results/expanded_scenario_results_*.json',
    'results/framework_performance_report_*.json'
]
for pattern in result_files:
    files = glob.glob(pattern)
    print(f'{pattern}: {len(files)} files found')
"
```

### 2. Data Quality Verification
```python
# Execute data quality verification
from src.common_utils import DataQualityValidator

validator = DataQualityValidator()
validation_results = validator.validate_experiment_results('results/')
print(validation_results)
```

## Performance Optimization

### 1. Parallel Processing Setup
```python
# Parallel experiment execution (4 workers)
python run_cultural_sensitivity_experiments.py --parallel --workers 4
```

### 2. Memory Optimization
```python
# Batch size adjustment
python run_expanded_scenario_experiments.py --batch_size 10
```

## Troubleshooting

### 1. Ollama Connection Issues
```bash
# Check Ollama service status
ollama list

# Restart service
killall ollama
ollama serve
```

### 2. Memory Shortage Issues
- Reduce batch size (`--batch_size 5`)
- Use smaller models (`gemma2:2b` instead of `llama3.2:3b`)
- Check system memory and close other programs

### 3. Dependency Issues
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Resolve specific package issues
pip install --force-reinstall sentence-transformers
```

## Expected Execution Time

- Full experimental pipeline: 2-4 hours (depending on system specifications)
- Cultural sensitivity experiments: 30-60 minutes
- Extended scenario experiments: 45-90 minutes
- Adversarial robustness testing: 20-40 minutes
- Statistical analysis: 5-10 minutes

## Key Experiments for Paper Reproduction

### 1. Table 3 Reproduction (Cultural Sensitivity Analysis)
```bash
python run_cultural_sensitivity_experiments.py --output_table3
```

### 2. Figure 4 Reproduction (Framework Performance Comparison)
```bash
python analyze_framework_performance.py --generate_figure4
```

### 3. Table 5 Reproduction (Adversarial Robustness Results)
```bash
python adversarial_testing_system.py --output_table5
```

## License and Citation

This reproducibility package is provided under the MIT License. If you use it in your research, please cite as follows:

```bibtex
@article{ethical_llm_evaluation_2024,
  title={Comprehensive Evaluation Framework for Ethical Decision-Making in Large Language Models},
  author={Jinseok Seo},
  journal={[Journal]},
  year={2024}
}
```

## Support and Contact

- GitHub Issues: [Repository URL]
- Email: [Contact Email]
- Documentation: `docs/experimental_protocols_documentation.md`

## Version Information

- Package Version: 1.0.0
- Last Updated: January 2024
- Python Version: 3.8+
- Ollama Version: 0.1.0+