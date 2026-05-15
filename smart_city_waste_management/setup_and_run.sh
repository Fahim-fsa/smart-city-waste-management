#!/bin/bash

echo "======================================"
echo "  Smart City Waste Management Setup"
echo "======================================"

# 1. Create virtual environment
echo ""
echo "[1/5] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "[2/5] Installing dependencies..."
pip install -r requirements.txt

# 3. Run migrations
echo "[3/5] Running database migrations..."
python manage.py makemigrations users_app
python manage.py makemigrations citizen_reports_app
python manage.py makemigrations waste_management_app
python manage.py makemigrations notifications_app
python manage.py makemigrations analytics_app
python manage.py migrate

# 4. Seed sample data
echo "[4/5] Seeding sample data..."
python manage.py seed_data

# 5. Collect static files (optional for dev)
echo "[5/5] Setup complete!"

echo ""
echo "======================================"
echo "  Setup complete! Starting server..."
echo "======================================"
echo ""
echo "  Open: http://127.0.0.1:8000"
echo ""
echo "  Credentials:"
echo "  Admin:     admin@smartwaste.com / admin123"
echo "  Citizen:   rahim@example.com    / password123"
echo "  Volunteer: nasrin@example.com   / password123"
echo ""

python manage.py runserver
