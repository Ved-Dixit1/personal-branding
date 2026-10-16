#!/usr/bin/env bash
# Quick launcher for OmniBrand AI Studio
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "🎬 Starting OmniBrand AI Video Studio on http://localhost:8501 ..."
streamlit run app.py --server.port 8501 --server.headless true
