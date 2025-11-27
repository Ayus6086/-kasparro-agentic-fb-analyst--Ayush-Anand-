#!/bin/bash

# ============================================================
# Kasparro Agentic FB Analyst – Runner Script
# ============================================================

echo "🔹 Activating virtual environment..."
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

if [ $? -ne 0 ]; then
  echo "❌ Could not activate virtual environment."
  echo "Please run: python -m venv .venv"
  exit 1
fi

echo "🔹 Installing dependencies..."
pip install -r requirements.txt

echo "🔹 Running Agentic Pipeline..."
python -m src.orchestrator.run

echo "✅ Done! Outputs generated in: reports/ and logs/"
