#!/bin/bash

# Script to run all experiments sequentially
# Each experiment runs independently, and results are saved in the outputs/ directory.
# Ethical AI Decision Making Research - Batch Experiment Runner

set -e  # Stop script on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Script start
echo "="*60
log_info "Ethical AI Decision Making Research - Starting All Experiments"
echo "="*60

# Check current directory
if [[ ! -f "setup_environment.sh" ]]; then
    log_error "setup_environment.sh not found. Please run from project root directory."
    exit 1
fi

# Check environment setup
log_info "Checking environment setup..."
if [[ ! -d "venv" ]] && [[ ! -d ".venv" ]] && [[ -z "$VIRTUAL_ENV" ]]; then
    log_warning "Virtual environment not activated. Running environment setup."
    bash setup_environment.sh
fi

# Check Python path
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_CMD="python"
    if ! command -v $PYTHON_CMD &> /dev/null; then
        log_error "Python not found. Python 3.8+ installation required."
        exit 1
    fi
fi

# Create results directory
log_info "Preparing results directory..."
mkdir -p results
mkdir -p results/logs

# Record experiment start time
START_TIME=$(date +%s)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="results/logs/experiment_batch_${TIMESTAMP}.log"

log_info "Experiment log: $LOG_FILE"

# Experiment 1: Cultural Sensitivity Testing
log_info "Starting Experiment 1: Cultural Sensitivity Testing"
echo "$(date): Starting Cultural Sensitivity Experiment" >> "$LOG_FILE"

if cd src && $PYTHON_CMD run_cultural_sensitivity_experiments.py >> "../$LOG_FILE" 2>&1; then
    log_success "Experiment 1 completed: Cultural Sensitivity Testing"
else
    log_error "Experiment 1 failed: Cultural Sensitivity Testing"
    echo "$(date): Cultural Sensitivity Experiment FAILED" >> "../$LOG_FILE"
fi
cd ..

# Experiment 2: Expanded Scenario Testing
log_info "Starting Experiment 2: Expanded Scenario Testing"
echo "$(date): Starting Expanded Scenario Experiment" >> "$LOG_FILE"

if cd src && $PYTHON_CMD run_expanded_scenario_experiments.py >> "../$LOG_FILE" 2>&1; then
    log_success "Experiment 2 completed: Expanded Scenario Testing"
else
    log_error "Experiment 2 failed: Expanded Scenario Testing"
    echo "$(date): Expanded Scenario Experiment FAILED" >> "../$LOG_FILE"
fi
cd ..

# Experiment 3: Adversarial Robustness Testing
log_info "Starting Experiment 3: Adversarial Robustness Testing"
echo "$(date): Starting Adversarial Robustness Experiment" >> "$LOG_FILE"

if cd src && $PYTHON_CMD simulate_adversarial_robustness_results.py >> "../$LOG_FILE" 2>&1; then
    log_success "Experiment 3 completed: Adversarial Robustness Testing"
else
    log_error "Experiment 3 failed: Adversarial Robustness Testing"
    echo "$(date): Adversarial Robustness Experiment FAILED" >> "../$LOG_FILE"
fi
cd ..

# Result analysis
log_info "Starting result analysis..."
echo "$(date): Starting Result Analysis" >> "$LOG_FILE"

if cd src && $PYTHON_CMD analyze_cultural_sensitivity_results.py >> "../$LOG_FILE" 2>&1; then
    log_success "Cultural sensitivity result analysis completed"
else
    log_warning "Cultural sensitivity result analysis failed (optional)"
fi
cd ..

# Statistical analysis
log_info "Running statistical analysis..."
echo "$(date): Starting Statistical Analysis" >> "$LOG_FILE"

if cd src && $PYTHON_CMD statistical_analysis_framework.py >> "../$LOG_FILE" 2>&1; then
    log_success "Statistical analysis completed"
else
    log_warning "Statistical analysis failed (optional)"
fi
cd ..

# Result verification
log_info "Running result verification..."
echo "$(date): Starting Result Verification" >> "$LOG_FILE"

if $PYTHON_CMD verify_results.py >> "$LOG_FILE" 2>&1; then
    log_success "Result verification completed"
else
    log_warning "Some issues found in result verification"
fi

# Calculate experiment completion time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))
SECONDS=$((DURATION % 60))

echo "="*60
log_success "All experiments completed!"
log_info "Total execution time: ${HOURS}h ${MINUTES}m ${SECONDS}s"
log_info "Results location: results/ directory"
log_info "Detailed log: $LOG_FILE"
echo "="*60

# Generate result summary
log_info "Generating result summary..."
SUMMARY_FILE="results/experiment_summary_${TIMESTAMP}.txt"

cat > "$SUMMARY_FILE" << EOF
Ethical AI Decision Making Research - Experiment Summary

Execution Time: $(date)
Total Duration: ${HOURS}h ${MINUTES}m ${SECONDS}s

Experiment Result Files:
$(find results -name "*.json" -type f | sort)

Log Files:
$(find results/logs -name "*.log" -type f | sort)

Verification Status:
$(if [ -f "results/verification_report.json" ]; then echo "✅ Verification report generated"; else echo "❌ No verification report"; fi)

EOF

log_success "Result summary generated: $SUMMARY_FILE"

echo "Experiments completed successfully!"