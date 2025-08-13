#!/bin/bash

# run_experiment.sh - Ethical AI Experiment Execution Script
# Usage: bash scripts/run_experiment.sh <exp_id> [--seed SEED] [--config CONFIG] [--sha-log]

set -e  # Exit script on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default settings
SEED=42
CONFIG="config/config.yaml"
SHA_LOG=false
EXP_ID=""

# Help function
show_help() {
    echo "Ethical AI Experiment Execution Script"
    echo ""
    echo "Usage:"
    echo "  bash scripts/run_experiment.sh <exp_id> [options]"
    echo ""
    echo "Experiment IDs:"
    echo "  1, exp1, experiment1    - Prompt Segmentation Experiment"
    echo "  2, exp2, experiment2    - Ethical Framework Analysis"
    echo "  3, exp3, experiment3    - Complex Scenario Stress Test"
    echo ""
    echo "Options:"
    echo "  --seed SEED             Set seed value (default: 42)"
    echo "  --config CONFIG         Configuration file path (default: config/config.yaml)"
    echo "  --sha-log               Output Git SHA log before and after execution"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  bash scripts/run_experiment.sh 1"
    echo "  bash scripts/run_experiment.sh exp2 --seed 123"
    echo "  bash scripts/run_experiment.sh 3 --config custom_config.yaml --sha-log"
    echo ""
    echo "Results save path:"
    echo "  - Experiment results: data/results/"
    echo "  - Log files: data/results/experiment_<id>_<timestamp>.log"
    echo "  - Statistics data: data/stats_combined.csv"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        --seed)
            SEED="$2"
            shift 2
            ;;
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --sha-log)
            SHA_LOG=true
            shift
            ;;
        -*)
            echo -e "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$EXP_ID" ]]; then
                EXP_ID="$1"
            else
                echo -e "${RED}Error: Too many arguments provided${NC}"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate experiment ID
if [[ -z "$EXP_ID" ]]; then
    echo -e "${RED}Error: Experiment ID is required${NC}"
    show_help
    exit 1
fi

# Normalize experiment ID
case "$EXP_ID" in
    1|exp1|experiment1)
        EXP_ID="1"
        EXP_NAME="Prompt Segmentation Experiment"
        EXP_FILE="src/experiment1.py"
        ;;
    2|exp2|experiment2)
        EXP_ID="2"
        EXP_NAME="Ethical Framework Analysis"
        EXP_FILE="src/experiment2.py"
        ;;
    3|exp3|experiment3)
        EXP_ID="3"
        EXP_NAME="Complex Scenario Stress Test"
        EXP_FILE="src/experiment3.py"
        ;;
    *)
        echo -e "${RED}Error: Invalid experiment ID: $EXP_ID${NC}"
        echo "Valid experiment IDs: 1, 2, 3, exp1, exp2, exp3, experiment1, experiment2, experiment3"
        exit 1
        ;;
esac

# Check file existence
if [[ ! -f "$EXP_FILE" ]]; then
    echo -e "${RED}Error: Cannot find experiment file: $EXP_FILE${NC}"
    exit 1
fi

if [[ ! -f "$CONFIG" ]]; then
    echo -e "${YELLOW}Warning: Cannot find configuration file: $CONFIG${NC}"
    echo "Proceeding with default settings."
fi

# Create results directory
mkdir -p data/results

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="data/results/experiment_${EXP_ID}_${TIMESTAMP}.log"

# Output pre-execution information
echo -e "${BLUE}=== Ethical AI Experiment Execution ===${NC}"
echo -e "Experiment ID: ${GREEN}$EXP_ID${NC}"
echo -e "Experiment Name: ${GREEN}$EXP_NAME${NC}"
echo -e "Experiment File: ${GREEN}$EXP_FILE${NC}"
echo -e "Seed Value: ${GREEN}$SEED${NC}"
echo -e "Configuration File: ${GREEN}$CONFIG${NC}"
echo -e "Log File: ${GREEN}$LOG_FILE${NC}"
echo -e "Start Time: ${GREEN}$(date)${NC}"
echo ""

# Git SHA log (before execution)
if [[ "$SHA_LOG" == "true" ]]; then
    echo -e "${BLUE}=== Git Status Before Execution ===${NC}"
    echo -e "Current Commit: ${GREEN}$(git rev-parse HEAD)${NC}"
    echo -e "Branch: ${GREEN}$(git branch --show-current)${NC}"
    echo -e "Status: ${GREEN}$(git status --porcelain | wc -l) changed files${NC}"
    echo ""
fi

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed${NC}"
    exit 1
fi

# Check required packages
echo -e "${BLUE}Checking Python environment...${NC}"
if [[ -f "requirements.txt" ]]; then
    python3 -m pip install -q -r requirements.txt
fi

# Execute experiment
echo -e "${BLUE}=== Starting Experiment Execution ===${NC}"
echo "Execution command: python3 $EXP_FILE"
echo ""

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export EXPERIMENT_SEED="$SEED"
export CONFIG_FILE="$CONFIG"

# Execute experiment (save output to log file)
if python3 "$EXP_FILE" 2>&1 | tee "$LOG_FILE"; then
    echo ""
    echo -e "${GREEN}=== Experiment Completed ===${NC}"
    echo -e "End Time: ${GREEN}$(date)${NC}"
    echo -e "Log File: ${GREEN}$LOG_FILE${NC}"
    
    # Check result files
    if [[ -f "data/stats_combined.csv" ]]; then
        echo -e "Statistics Data: ${GREEN}data/stats_combined.csv${NC}"
        echo -e "Total Records: ${GREEN}$(tail -n +2 data/stats_combined.csv | wc -l)${NC}"
    fi
    
    # Check latest result files
    LATEST_RESULT=$(find data/results -name "*.json" -o -name "*.csv" | head -1)
    if [[ -n "$LATEST_RESULT" ]]; then
        echo -e "Latest Result: ${GREEN}$LATEST_RESULT${NC}"
    fi
    
    EXIT_CODE=0
else
    echo ""
    echo -e "${RED}=== Experiment Failed ===${NC}"
    echo -e "Error Log: ${RED}$LOG_FILE${NC}"
    echo "Last 10 lines of log:"
    echo -e "${YELLOW}"
    tail -10 "$LOG_FILE"
    echo -e "${NC}"
    EXIT_CODE=1
fi

# Git SHA log (after execution)
if [[ "$SHA_LOG" == "true" ]]; then
    echo ""
    echo -e "${BLUE}=== Git Status After Execution ===${NC}"
    echo -e "Current Commit: ${GREEN}$(git rev-parse HEAD)${NC}"
    echo -e "Status: ${GREEN}$(git status --porcelain | wc -l) changed files${NC}"
    
    # Check for newly created files
    NEW_FILES=$(git status --porcelain | grep "^??" | wc -l)
    if [[ $NEW_FILES -gt 0 ]]; then
        echo -e "New Files: ${YELLOW}$NEW_FILES files${NC}"
        git status --porcelain | grep "^??" | head -5
    fi
fi

echo ""
echo -e "${BLUE}=== Experiment Summary ===${NC}"
echo -e "Experiment ID: $EXP_ID ($EXP_NAME)"
echo -e "Seed Value: $SEED"
echo -e "Execution Time: $(date)"
echo -e "Log File: $LOG_FILE"
echo -e "Exit Code: $EXIT_CODE"

exit $EXIT_CODE