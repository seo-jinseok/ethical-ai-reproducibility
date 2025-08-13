# Quick Start Guide

## 🚀 Reproduce Paper Results in 3 Steps

### Step 1: Setup Environment
```bash
# Make setup script executable
chmod +x setup_environment.sh

# Run automated setup
./setup_environment.sh
```

### Step 2: Run Experiments
```bash
cd src

# Cultural sensitivity experiments (~30-60 min)
python run_cultural_sensitivity_experiments.py

# Expanded scenario experiments (~45-90 min)
python run_expanded_scenario_experiments.py

# Adversarial robustness testing (~20-40 min)
python adversarial_testing_system.py

# Expert panel evaluation (~10-20 min)
python expert_panel_integration.py
```

### Step 3: Analyze Results
```bash
# Generate analysis reports
python analyze_cultural_sensitivity_results.py
python analyze_framework_performance.py
python analyze_adversarial_robustness_results.py

# Verify all results
cd ..
python verify_results.py
```

## 📊 Expected Outputs

After completion, check the `results/` directory for:
- `cultural_sensitivity_experiment_results_*.json`
- `expanded_scenario_results_*.json`
- `adversarial_robustness_analysis_report_*.json`
- `framework_performance_report_*.json`
- `verification_report.json`

## ⚡ Quick Test

To verify setup without running full experiments:
```bash
cd src
python -c "import enhanced_ethical_evaluator; print('Setup successful!')"
```

## 🔧 Troubleshooting

**Ollama not found?**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

**Python dependencies?**
```bash
pip install --upgrade -r requirements.txt
```

**Memory issues?**
```bash
# Use smaller model
python run_cultural_sensitivity_experiments.py --model gemma2:2b
```

## 📚 More Information

- [Full Documentation](README.md)
- [Methodology Summary](docs/methodology_summary.md)
- [Detailed Protocols](docs/experimental_protocols.md)