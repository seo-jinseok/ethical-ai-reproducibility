# Ethical AI Decision-Making Research Reproducibility Package (Complete Integrated Version)

## 📋 Overview

This repository provides a **complete integrated version** containing all necessary code, data, and environment configurations to reproduce the experiments from the paper "Game-Based Ethical Decision Making in LLMs: Cross-Cultural Frameworks and Prompt Engineering".

### ✨ Integration Completed
- 🔧 Core CAI (Cultural Adaptability Index) module included
- 📊 All experimental results and analysis tools integrated
- 📚 Complete documentation and guides provided
- 🧪 Validated experimental scripts and reproducibility tools
- 📈 All data and results used in the actual paper included

## 🎯 Research Objectives

- Evaluate ethical decision-making capabilities of Large Language Models (LLMs)
- Comparative analysis of ethical frameworks in multicultural contexts
- Study the impact of prompt engineering on ethical judgment
- Develop methods for detecting and mitigating cultural bias

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/seo-jinseok/ethical-ai-reproducibility.git
cd ethical-ai-reproducibility

# Run automated environment setup
bash setup_environment.sh
```

### 2. Run Experiments
```bash
# Activate virtual environment
source venv/bin/activate

# Run all experiments
bash scripts/reproduce.sh

# Run individual experiments
bash scripts/run_experiment.sh 1  # Prompt granularity experiment
bash scripts/run_experiment.sh 2  # Multicultural framework experiment
bash scripts/run_experiment.sh 3  # Complex scenario stress test
```

### 3. Check Results
```bash
# Check result files
ls results/

# Verify reproducibility
bash scripts/reproduce.sh --verify-only
```

## 📁 Project Structure

```
ethical-ai-reproducibility/
├── 📄 README.md                     # This file
├── 🔧 setup_environment.sh          # Automated environment setup
├── 🚀 QUICK_START.md                # Quick start guide
├── 📄 LICENSE                       # MIT License
├── 🔍 verify_results.py             # Results verification script
├── 📝 .gitignore                    # Git ignore file
│
├── 📚 docs/                          # Documentation
│   ├── methodology.md               # Research methodology
│   ├── methodology_summary.md       # Methodology summary
│   ├── experimental_protocols.md    # Experimental protocols
│   └── reproducibility_guide.md     # Detailed reproduction guide
│
├── 🔬 scripts/                       # Experiment execution scripts
│   ├── reproduce.sh                 # Reproducibility verification script
│   ├── run_experiment.sh            # Individual experiment execution
│   ├── run_all_experiments.sh       # Batch execution of all experiments
│   └── verify_outputs.py            # Result verification
│
├── 💻 src/                           # Core implementation code
│   ├── experiment1.py               # Experiment 1: Prompt granularity
│   ├── experiment2.py               # Experiment 2: Multicultural frameworks
│   ├── experiment3.py               # Experiment 3: Stress testing
│   ├── cai.py                       # Cultural Adaptability Index
│   ├── cai_metrics.py               # CAI metric calculations
│   ├── common_utils.py              # Common utilities
│   ├── culturally_aware_scenarios.py # Culturally aware scenario generator
│   ├── enhanced_cultural_bias_system.py # Enhanced cultural bias detection
│   └── western_bias_acknowledgment.py # Western bias acknowledgment system
│
├── 📊 data/                          # Experimental data
│   ├── ethical_scenarios.csv        # Ethical scenarios
│   ├── moral_dataset.csv            # Moral judgment data
│   └── scenario_meta.json           # Scenario metadata
│
├── 📈 results/                       # Experimental results (actual results included)
│   ├── cultural_sensitivity_experiment_results_*.json
│   ├── cultural_sensitivity_analysis_report_*.json
│   ├── expanded_scenario_results_*.json
│   ├── adversarial_robustness_analysis_report_*.json
│   ├── statistical_analysis_report_*.json
│   ├── framework_performance_*.json
│   ├── simulated_*.json
│   └── verification_report.json
│
└── ⚙️ config/                        # Configuration files
    ├── config.yaml                  # Experiment configuration
    ├── pyproject.toml               # Project configuration
    └── requirements.txt             # Python dependencies
```

## 🔧 Advanced Usage

### Customizing CAI Metrics

```python
from src.cai_metrics import CAIMetrics

# Initialize CAI metrics
cai_metrics = CAIMetrics()

# Set custom cultural weights
custom_weights = {
    'my_culture': {
        'individualism': 0.6,
        'hierarchy': 0.4,
        'uncertainty_avoidance': 0.5
    }
}
cai_metrics.add_cultural_framework('my_culture', custom_weights)

# Calculate CAI score
responses = ["response1", "response2", "response3"]
cai_score = cai_metrics.calculate_cai(responses, 'my_culture')
print(f"CAI Score: {cai_score}")
```

### Batch Experiment Execution

```bash
# Run all experiments sequentially
./scripts/run_all_experiments.sh

# Run experiments for specific model only
python3 src/experiment1.py --model llama-3.1-8b --cultural-framework eastern

# Generate culturally aware scenarios
python3 src/culturally_aware_scenarios.py

# Detect cultural bias
python3 src/enhanced_cultural_bias_system.py
```

### Custom Statistical Analysis

```python
from src.common_utils import calculate_statistics

# Calculate basic statistics
stats = calculate_statistics(data)

# Calculate effect size using Cohen's d
effect_size = (mean1 - mean2) / pooled_std

# Calculate confidence interval
import scipy.stats as stats
ci_lower, ci_upper = stats.t.interval(0.95, len(data)-1, 
                                     loc=np.mean(data), 
                                     scale=stats.sem(data))
```

### Extending Cultural Frameworks

```python
from src.enhanced_cultural_bias_system import CulturalBiasDetector
from src.culturally_aware_scenarios import CulturallyAwareScenarios

# Initialize cultural bias detector
bias_detector = CulturalBiasDetector()

# Define custom cultural parameters
custom_cultural_params = {
    "collectivism_score": 0.8,
    "power_distance": 0.6,
    "long_term_orientation": 0.7,
    "uncertainty_avoidance": 0.5
}

# Generate culturally aware scenarios
scenario_generator = CulturallyAwareScenarios()
custom_scenarios = scenario_generator.generate_scenarios(
    cultural_framework="custom",
    parameters=custom_cultural_params
)
```

## 🔬 Experimental Modules

### Experiment 1: Prompt Granularity Effect Analysis
- **Purpose**: Analyze the impact of prompt structure on ethical judgment
- **Execution**: `python src/experiment1.py`
- **Results**: Performance comparison by prompt type

### Experiment 2: Multicultural Ethical Framework Comparison
- **Purpose**: Compare Western, Confucian, Ubuntu, and Buddhist ethical frameworks
- **Execution**: `python src/experiment2.py`
- **Results**: Analysis of cultural differences in ethical judgment

### Experiment 3: Complex Scenario Stress Testing
- **Purpose**: Evaluate model performance on complex and ambiguous ethical dilemmas
- **Execution**: `python src/experiment3.py`
- **Results**: Assessment of model robustness and consistency

## 📊 Key Metrics

### Cultural Adaptability Index (CAI)
- Core indicator measuring cultural adaptability
- Calculation method: `python src/cai_metrics.py`
- Range: 0.0 (low) ~ 1.0 (high)

### Statistical Significance Testing
- ANOVA, Kruskal-Wallis tests
- Effect size (Cohen's d, η²)
- Multiple comparison correction (Bonferroni)

## 🛠️ System Requirements

### Essential Requirements
- **Python**: 3.12 or higher
- **Memory**: Minimum 8GB RAM (Recommended: 16GB)
- **Storage**: 10GB or more
- **Operating System**: macOS, Linux, Windows

### Recommended Hardware
- **GPU**: CUDA-supported GPU (optional, for local LLM execution)
- **CPU**: Multi-core processor (for parallel processing)

## 🔧 Detailed Environment Setup

### 1. Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Local LLM Setup (Optional)
```bash
# Install Ollama (macOS)
brew install ollama

# Download models
ollama pull llama3.2:3b
ollama pull gemma2:2b
```

## 📈 Result Interpretation

### Experimental Result Files
- `results/cultural_sensitivity_experiment_results_*.json`: Cultural sensitivity experiment results
- `results/cultural_sensitivity_analysis_report_*.json`: Cultural sensitivity analysis reports
- `results/expanded_scenario_results_*.json`: Expanded scenario test results
- `results/adversarial_robustness_analysis_report_*.json`: Adversarial robustness analysis
- `results/statistical_analysis_report_*.json`: Statistical analysis reports
- `results/framework_performance_*.json`: Framework performance comparisons
- `results/verification_report.json`: Overall verification report

### Additional Result Files
- `results/simulated_*.json`: Simulated experiment results
- `results/load_summary.json`: Load testing summary

## 🔍 Reproducibility Verification

### Automated Verification
```bash
# Complete reproducibility verification
bash scripts/reproduce.sh

# Verify existing results only
bash scripts/reproduce.sh --verify-only

# Generate new baseline hashes
bash scripts/reproduce.sh --generate-hashes
```

### Manual Verification
```bash
# Check individual file hashes
shasum -a 256 data/moral_dataset.csv
shasum -a 256 data/ethical_scenarios.csv
shasum -a 256 results/verification_report.json

# Verify results using built-in script
python verify_results.py
```

## 🤝 How to Contribute

1. **Issue Reporting**: Report bugs or improvements to GitHub Issues
2. **Pull Requests**: Code improvements or new feature additions
3. **Documentation**: Improve usage instructions or explanations
4. **Testing**: Reproducibility testing in various environments

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 📞 Contact

- **e-mail**: jsseo@deu.ac.kr

## 🙏 Citation

If you use this research, please cite as follows:

```bibtex
@article{ethical_ai_2025,
  title={Game-Based Ethical Decision Making in LLMs: Cross-Cultural Frameworks and Prompt Engineering},
  author={Jinseok Seo},
  journal={[Submitted]},
  year={2025},
  doi={[DOI]}
}
```

## 📝 Change Log

- **v1.0.0** (2025-01-28): Initial public release
- All experimental code and data included
- Complete reproducibility verification system
- Detailed documentation completed

---

**Note**: This research was conducted with respect for AI ethics and cultural diversity. All experiments were designed to minimize bias and ensure fairness.