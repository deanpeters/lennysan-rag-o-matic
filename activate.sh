#!/bin/bash

# LennySan RAG-o-Matic - Quick Start
# This script activates the project's Python virtual environment so that
# the exact dependencies in requirements.txt are on your PATH.
# Use this before running explore.py or index_corpus.py to avoid
# "ModuleNotFoundError" errors from missing packages.
# Why a virtual environment matters:
# - It keeps project-specific libraries separate from your system Python.
# - It prevents version conflicts with other tools on your machine.
# - It makes "works on my machine" setups more reproducible for others.

# Detect whether this script is being sourced (bash/zsh compatible).
is_sourced=0
if [[ -n "${ZSH_EVAL_CONTEXT:-}" ]]; then
  case "$ZSH_EVAL_CONTEXT" in
    *:file) is_sourced=1 ;;
  esac
fi
if [[ -n "${BASH_SOURCE:-}" && "${BASH_SOURCE[0]}" != "$0" ]]; then
  is_sourced=1
fi

if [[ "$is_sourced" -ne 1 ]]; then
  echo "⚠️  This script must be sourced to keep the environment active."
  echo "Run: source activate.sh"
  exit 1
fi

echo "🚀 LennySan RAG-o-Matic v0.5"
echo ""

# Activate virtual environment for this repo
source .venv/bin/activate

echo "✅ Environment activated"
echo ""
echo "Try these queries:"
echo "  python explore.py 'What does Lenny say about pricing?'"
echo "  python explore.py 'How do you find product-market fit?'"
echo "  python explore.py 'What are common enterprise sales mistakes?'"
echo ""
echo "When done:"
echo "  deactivate"
echo ""
