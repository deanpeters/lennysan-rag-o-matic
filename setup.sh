#!/bin/bash

# LennySan RAG-o-Matic v0.6 Setup Script
# CONFIGS.yaml: Centralize defaults and paths

set -e  # Exit on any error

# Create logs directory
mkdir -p logs

# Setup logging with timestamp
LOG_FILE="logs/setup_$(date +%Y%m%d_%H%M%S).log"

# Redirect all output to both console and log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "======================================"
echo "LennySan RAG-o-Matic v0.6 Setup"
echo "======================================"
echo ""
echo "📋 Logging to: $LOG_FILE"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# PREFLIGHT CHECKS
# ============================================

echo "🔍 Running preflight checks..."
echo ""

# Check for Mac (v0.1 is Mac-only)
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}⚠️  Warning: This script is designed for Mac. You're on $OSTYPE${NC}"
    echo "Windows support coming in v3.0"
    echo "You can continue, but you may encounter issues."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found${NC}"
    echo "Install Git: https://git-scm.com/downloads"
    exit 1
fi
echo -e "${GREEN}✅ Git found${NC}"

# Check for Python 3.9+
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Install Python 3.9+: https://python.org/downloads"
    if command -v brew &> /dev/null; then
        echo "Or via Homebrew: brew install python@3.11"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}❌ Python 3.9+ required. Found: $PYTHON_VERSION${NC}"
    echo "Upgrade Python: https://python.org/downloads"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check for Anthropic API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ ANTHROPIC_API_KEY not found${NC}"
    echo ""
    echo "Set your API key in your shell profile:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-...'"
    echo ""
    echo "Add to ~/.bashrc or ~/.zshrc, then reload:"
    echo "  source ~/.bashrc  (or source ~/.zshrc)"
    echo ""
    echo "Get an API key: https://console.anthropic.com/"
    exit 1
fi
echo -e "${GREEN}✅ ANTHROPIC_API_KEY found${NC}"

# Check for episodes directory
if [ ! -d "episodes" ]; then
    echo -e "${RED}❌ 'episodes' directory not found${NC}"
    echo "Make sure you're running this from the repo root"
    exit 1
fi
echo -e "${GREEN}✅ Episodes directory found${NC}"

# Check for Homebrew (optional but helpful)
if command -v brew &> /dev/null; then
    echo -e "${GREEN}✅ Homebrew detected${NC}"
else
    echo -e "${YELLOW}💡 Homebrew not found (optional)${NC}"
    echo "   Consider installing: https://brew.sh"
fi

echo ""
echo -e "${GREEN}All prerequisites met!${NC}"
echo ""

# ============================================
# DIRECTORY STRUCTURE
# ============================================

echo "📁 Creating directory structure..."

mkdir -p data/chroma_db

echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# ============================================
# PYTHON VIRTUAL ENVIRONMENT
# ============================================

echo "🐍 Setting up Python virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

source .venv/bin/activate

echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# ============================================
# PYTHON DEPENDENCIES
# ============================================

echo "📦 Installing Python dependencies..."
echo "This may take a few minutes..."
echo ""

pip install --upgrade pip --quiet
pip install -r requirements.txt

echo ""
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# ============================================
# INDEXING
# ============================================

echo "🔍 Indexing corpus in ChromaDB..."
echo "This will take 5-10 minutes."
echo ""
echo "💡 To prevent your Mac from sleeping during indexing:"
echo "   We'll use 'caffeinate' to keep the system awake."
echo ""
echo "☕ Perfect time for that coffee break!"
echo ""

# Use caffeinate on Mac to prevent sleep during long operation
if [[ "$OSTYPE" == "darwin"* ]]; then
    caffeinate -i python3 index_corpus.py
else
    python3 index_corpus.py
fi

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Indexing failed${NC}"
    echo "Check the error messages above"
    exit 1
fi

echo ""

# Make explore.py executable
chmod +x explore.py

# ============================================
# CLEANUP & FINAL INSTRUCTIONS
# ============================================

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "You're ready to explore Lenny's podcast corpus."
echo ""
echo "Try it out:"
echo "  python explore.py 'What does Lenny say about pricing?'"
echo ""
echo "More examples:"
echo "  python explore.py 'How do you find product-market fit?'"
echo "  python explore.py 'What are common enterprise sales mistakes?'"
echo ""
echo "Remember:"
echo "  - Using Claude Haiku (cheapest model)"
echo "  - Queries cost ~\$0.001-0.005 each"
echo "  - This is v0.1 - expect rough edges"
echo ""
echo "📋 Logs saved to: $LOG_FILE"
echo "   (If anything went wrong, check the logs for details)"
echo ""
echo "Next steps:"
echo "  - Try different queries"
echo "  - Open issues if you find bugs"
echo "  - v0.5 will add model switching"
echo ""
echo "Have fun! 🚀"
echo ""
echo "To deactivate the virtual environment later:"
echo "  deactivate"
