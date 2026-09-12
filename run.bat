@echo off
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt
echo.
echo Starting Agentic AI Security Pipeline...
echo Open http://localhost:8000 in your browser
echo.
python app.py
