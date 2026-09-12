#!/usr/bin/env bash
set -e
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo ""
echo "Starting Agentic AI Security Pipeline..."
echo "Open http://localhost:8000 in your browser"
echo ""
python app.py
