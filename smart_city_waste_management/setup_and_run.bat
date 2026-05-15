@echo off
echo ======================================
echo   Smart City Waste Management Setup
echo ======================================

echo.
echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/5] Installing dependencies...
pip install -r requirements.txt

echo [3/5] Running migrations...
python manage.py makemigrations users_app
python manage.py makemigrations citizen_reports_app
python manage.py makemigrations waste_management_app
python manage.py makemigrations notifications_app
python manage.py makemigrations analytics_app
python manage.py migrate

echo [4/5] Seeding sample data...
python manage.py seed_data

echo [5/5] Done!
echo.
echo ======================================
echo   Open: http://127.0.0.1:8000
echo   Admin:     admin@smartwaste.com / admin123
echo   Citizen:   rahim@example.com    / password123
echo   Volunteer: nasrin@example.com   / password123
echo ======================================
echo.

python manage.py runserver
pause
