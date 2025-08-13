#!/bin/bash

# reproduce.sh - Ethical AI Experiment Reproducibility Verification Script
# Usage: bash scripts/reproduce.sh [--verify-only] [--generate-hashes]

set -e  # Exit script on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default settings
VERIFY_ONLY=false
GENERATE_HASHES=false
OUTPUT_DIR="outputs"
HASH_FILE="expected_hashes.sha256"
TEMP_HASH_FILE="temp_hashes.sha256"

# Help function
show_help() {
    echo "Ethical AI Experiment Reproducibility Verification Script"
    echo ""
    echo "Usage:"
    echo "  bash scripts/reproduce.sh [options]"
    echo ""
    echo "Options:"
    echo "  --verify-only           Verify hashes of existing result files only (no re-run)"
    echo "  --generate-hashes       Generate new baseline hash file"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Process:"
    echo "  1. Run all experiments (call run_experiment.sh)"
    echo "  2. Calculate SHA256 hashes of result files"
    echo "  3. Compare with baseline hashes for reproducibility verification"
    echo "  4. Return non-zero code on verification failure"
    echo ""
    echo "Files to verify:"
    echo "  - data/moral_dataset.csv"
    echo "  - data/stats_combined.csv"
    echo "  - Experiment result log files"
    echo ""
    echo "Examples:"
    echo "  bash scripts/reproduce.sh                    # Full reproducibility verification"
    echo "  bash scripts/reproduce.sh --verify-only      # Verify existing results only"
    echo "  bash scripts/reproduce.sh --generate-hashes  # Generate new baseline hashes"
}

# Argument parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        --verify-only)
            VERIFY_ONLY=true
            shift
            ;;
        --generate-hashes)
            GENERATE_HASHES=true
            shift
            ;;
        -*)
            echo -e "${RED}Error: Unknown option $1${NC}"
            show_help
            exit 1
            ;;
        *)
            echo -e "${RED}Error: Unexpected argument $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

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

# Hash calculation function
calculate_hashes() {
    local hash_file="$1"
    log_info "Calculating SHA256 hashes of result files..."
    
    # Initialize hash file
    > "$hash_file"
    
    # Calculate hashes of core data files
    local files_to_hash=(
        "data/moral_dataset.csv"
        "data/stats_combined.csv"
    )
    
    # Add latest experiment result log files (max 3)
    if [[ -d "data/results" ]]; then
        local log_files=()
        while IFS= read -r -d '' file; do
            log_files+=("$file")
        done < <(find data/results -name "*.log" -type f -print0)
        
        # Select only up to 3 files
        local count=0
        for file in "${log_files[@]}"; do
            if [[ $count -lt 3 ]]; then
                files_to_hash+=("$file")
                count=$((count + 1))
            else
                break
            fi
        done
    fi
    
    # Calculate hash for each file
    for file in "${files_to_hash[@]}"; do
        if [[ -f "$file" ]]; then
            local hash=$(shasum -a 256 "$file" | cut -d' ' -f1)
            echo "$hash  $file" >> "$hash_file"
            log_info "Hash calculation completed: $file"
        else
            log_warning "File not found: $file"
        fi
    done
    
    log_success "Hash calculation completed: $hash_file"
}

# Hash verification function
verify_hashes() {
    local expected_file="$1"
    local actual_file="$2"
    
    if [[ ! -f "$expected_file" ]]; then
        log_error "Baseline hash file not found: $expected_file"
        log_info "Use --generate-hashes option to generate new baseline hashes"
        return 1
    fi
    
    if [[ ! -f "$actual_file" ]]; then
        log_error "Actual hash file not found: $actual_file"
        return 1
    fi
    
    log_info "Verifying hashes..."
    
    local verification_failed=false
    local total_files=0
    local matched_files=0
    
    # Verify each line of baseline hash file
    while IFS= read -r line; do
        if [[ -z "$line" || "$line" =~ ^#.* ]]; then
            continue  # Skip empty lines or comments
        fi
        
        local expected_hash=$(echo "$line" | cut -d' ' -f1)
        local file_path=$(echo "$line" | cut -d' ' -f3-)
        
        total_files=$((total_files + 1))
        
        # Find hash of corresponding file in actual hash file
        local actual_hash=$(grep "$file_path" "$actual_file" 2>/dev/null | cut -d' ' -f1)
        
        if [[ -z "$actual_hash" ]]; then
            log_error "Hash not found for file: $file_path"
            verification_failed=true
        elif [[ "$expected_hash" == "$actual_hash" ]]; then
            log_success "Hash match: $file_path"
            matched_files=$((matched_files + 1))
        else
            log_error "Hash mismatch: $file_path"
            log_error "  Expected: $expected_hash"
            log_error "  Actual: $actual_hash"
            verification_failed=true
        fi
    done < "$expected_file"
    
    echo ""
    log_info "Verification result: $matched_files/$total_files files matched"
    
    if [[ "$verification_failed" == "true" ]]; then
        log_error "Reproducibility verification failed!"
        return 1
    else
        log_success "All file hashes match. Reproducibility verification successful!"
        return 0
    fi
}

# Experiment execution function
run_experiments() {
    log_info "Running all experiments..."
    
    local experiments=(1 2 3)
    local failed_experiments=()
    
    for exp_id in "${experiments[@]}"; do
        log_info "Running experiment $exp_id..."
        
        if bash scripts/run_experiment.sh "$exp_id" --seed 42; then
            log_success "Experiment $exp_id completed"
        else
            log_error "Experiment $exp_id failed"
            failed_experiments+=("$exp_id")
        fi
    done
    
    if [[ ${#failed_experiments[@]} -gt 0 ]]; then
        log_error "Failed experiments: ${failed_experiments[*]}"
        return 1
    else
        log_success "All experiments completed"
        return 0
    fi
}

# Main execution logic
main() {
    echo -e "${BLUE}=== Ethical AI Experiment Reproducibility Verification ===${NC}"
    echo -e "Start time: ${GREEN}$(date)${NC}"
    echo ""
    
    # Check script existence
    if [[ ! -f "scripts/run_experiment.sh" ]]; then
        log_error "run_experiment.sh script not found"
        exit 1
    fi
    
    # New baseline hash generation mode
    if [[ "$GENERATE_HASHES" == "true" ]]; then
        log_info "New baseline hash generation mode"
        
        if [[ "$VERIFY_ONLY" == "false" ]]; then
            run_experiments || exit 1
        fi
        
        calculate_hashes "$HASH_FILE"
        log_success "New baseline hash file generated: $HASH_FILE"
        exit 0
    fi
    
    # Verification only mode
    if [[ "$VERIFY_ONLY" == "true" ]]; then
        log_info "Verification only mode (no experiment re-run)"
        calculate_hashes "$TEMP_HASH_FILE"
        verify_hashes "$HASH_FILE" "$TEMP_HASH_FILE"
        local verification_result=$?
        rm -f "$TEMP_HASH_FILE"
        exit $verification_result
    fi
    
    # Full reproducibility verification mode (default)
    log_info "Full reproducibility verification mode"
    
    # 1. Run experiments
    run_experiments || exit 1
    
    # 2. Calculate hashes
    calculate_hashes "$TEMP_HASH_FILE"
    
    # 3. Verify hashes
    verify_hashes "$HASH_FILE" "$TEMP_HASH_FILE"
    local verification_result=$?
    
    # 4. Clean up temporary files
    rm -f "$TEMP_HASH_FILE"
    
    echo ""
    echo -e "${BLUE}=== Reproducibility Verification Complete ===${NC}"
    echo -e "End time: ${GREEN}$(date)${NC}"
    
    if [[ $verification_result -eq 0 ]]; then
        log_success "Reproducibility verification successful!"
    else
        log_error "Reproducibility verification failed!"
    fi
    
    exit $verification_result
}

# Execute script
main "$@"