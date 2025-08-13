#!/bin/bash

# setup_environment.sh - Automated setup script for ethical AI research environment
# Usage: bash setup_environment.sh

set -e  # Exit script on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python found: $PYTHON_VERSION"
        
        # Check Python 3.12 or higher
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"; then
            log_success "Python version requirement met (3.12+)"
        else
            log_warning "Python 3.12 or higher is recommended. Current: $PYTHON_VERSION"
        fi
    else
        log_error "Python3 is not installed."
        exit 1
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        log_success "pip3 found"
    else
        log_error "pip3 is not installed."
        exit 1
    fi
    
    # Check Git (optional)
    if command -v git &> /dev/null; then
        log_success "Git found"
    else
        log_warning "Git is not installed. Installation is recommended for version control."
    fi
}

# Setup virtual environment
setup_virtual_environment() {
    log_info "Setting up Python virtual environment..."
    
    if [ -d "venv" ]; then
        log_warning "Existing virtual environment found. Reusing it."
    else
        log_info "Creating new virtual environment..."
        python3 -m venv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    log_success "Virtual environment activated"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip
    log_success "pip upgrade completed"
}

# Install dependencies
install_dependencies() {
    log_info "Installing Python packages..."
    
    if [ -f "config/requirements.txt" ]; then
        pip install -r config/requirements.txt
        log_success "Dependencies installation completed"
    else
        log_error "requirements.txt file not found."
        exit 1
    fi
}

# Setup data directories
setup_data_directories() {
    log_info "Setting up data directories..."
    
    # Create .gitkeep file in results directory
    touch results/.gitkeep
    
    # Set permissions
    chmod 755 scripts/*.sh 2>/dev/null || true
    
    log_success "Directory setup completed"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Test Python module imports
    python3 -c "
import pandas
import numpy
import scipy
import sklearn
import matplotlib
print('All required packages imported successfully')
" && log_success "Python package verification completed" || {
        log_error "Python package import failed"
        exit 1
    }
    
    # Check script execution permissions
    if [ -x "scripts/reproduce.sh" ]; then
        log_success "Script execution permissions verified"
    else
        log_warning "Setting script execution permissions..."
        chmod +x scripts/*.sh
    fi
}

# Show usage guide
show_usage_guide() {
    echo ""
    echo -e "${GREEN}=== Environment Setup Complete! ===${NC}"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Activate virtual environment:"
    echo -e "   ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo "2. Run all experiments:"
    echo -e "   ${YELLOW}bash scripts/reproduce.sh${NC}"
    echo ""
    echo "3. Run individual experiments:"
    echo -e "   ${YELLOW}bash scripts/run_experiment.sh 1${NC}  # Experiment 1"
    echo -e "   ${YELLOW}bash scripts/run_experiment.sh 2${NC}  # Experiment 2"
    echo -e "   ${YELLOW}bash scripts/run_experiment.sh 3${NC}  # Experiment 3"
    echo ""
    echo "4. Check results:"
    echo -e "   ${YELLOW}ls results/${NC}"
    echo ""
    echo "5. Verify reproducibility:"
    echo -e "   ${YELLOW}bash scripts/reproduce.sh --verify-only${NC}"
    echo ""
    echo "If you encounter any issues, please refer to docs/reproducibility_guide.md."
    echo ""
}

# Main execution function
main() {
    echo -e "${BLUE}=== Ethical AI Research Environment Setup ===${NC}"
    echo -e "Start time: ${GREEN}$(date)${NC}"
    echo ""
    
    check_requirements
    setup_virtual_environment
    install_dependencies
    setup_data_directories
    verify_installation
    show_usage_guide
    
    echo -e "${GREEN}Environment setup completed successfully!${NC}"
}

# Execute script
main "$@"