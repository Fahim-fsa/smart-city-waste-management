# 🌿 Smart City Waste Management

A full-featured Django web application for managing city waste — connecting citizens, volunteers, and administrators in one unified platform.

---

### 🧑🏼‍💻 Manual Setup
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations users_app
python manage.py makemigrations citizen_reports_app
python manage.py makemigrations waste_management_app
python manage.py makemigrations notifications_app
python manage.py makemigrations analytics_app
python manage.py migrate

python manage.py seed_data   # Load sample data
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🔑

| Role      | Email                      | Password     |
|-----------|----------------------------|--------------|
| Admin     | admin@smartwaste.com       | admin123     |
| Citizen   | rahim@example.com          | password123  |
| Volunteer | nasrin@example.com         | password123  |


Django Admin Panel: **http://127.0.0.1:8000/admin/**

---

## 📁 Project Structure

```
smart_city_waste_management/
├── smart_city_waste_management/   # Project config (settings, urls, wsgi)
├── users_app/                     # User auth, roles, dashboards
├── citizen_reports_app/           # Waste report submission & tracking
├── waste_management_app/          # Volunteer task management
├── notifications_app/             # In-app notifications
├── analytics_app/                 # Stats, charts & leaderboard
├── templates/                     # Global templates (base, home, about, contact)
├── static/                        # CSS & JS
├── media/                         # Uploaded images
└── manage.py
```

---

## 🧩 Features

### 👤 Users 
- Register / Login / Logout
- Role-based access: **Citizen**, **Volunteer**, **Admin**
- Profile management with image upload
- Change password

### 🤳🏼Citizen Reports
- Submit waste reports with photo & location
- Track report status (Pending → Approved → Assigned → In Progress → Completed)
- Admin approval / rejection
- Earn **10 reward points** per submission

### 🧹 Volunteer Tasks
- Volunteers update status & upload before/after images
- Complete a task to earn **50 reward points**


### 🔔 Notifications
- Automatic notifications on: report submission, approval, task assignment, cleanup completion
- Mark as read all at once

### 📊 Analytics
- Charts for Report Status Overview & User Breakdown
- Reward points leaderboard

---

