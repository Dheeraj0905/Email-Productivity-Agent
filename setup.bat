@echo off
echo Setting up Email Productivity Agent...

REM Create virtual environment
py -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Initialize database
py -c "from backend.database import init_database; init_database()"

REM Create .env if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please add your OpenAI API key.
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Add your OpenAI API key to .env file
echo 2. Run: streamlit run ui/app.py

pause
