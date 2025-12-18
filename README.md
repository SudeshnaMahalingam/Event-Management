# Event Scheduling & Resource Allocation System

A comprehensive, production-ready Flask web application for managing events and resources.
Featuring a premium UI, robust conflict detection, and secure authentication.

## Tech Stack
- **Backend:** Python 3, Flask .
- **Authentication:** Flask-Login
- **Frontend:** HTML5, Bootstrap 5, Custom CSS


## Features
- **Public Landing Page:** Modern "SaaS-style" home page.
- **Authentication:** Secure Signup and Login logic.
- **Interactive Dashboard:** Visual statistics and charts.
- **Conflict Detection:** Prevents resource double-booking.
- **Reporting:** Utilization tracking.

## Setup Instructions

1. **Clone/Navigate to the directory:**
   bash
   cd event_scheduler
   

2. **Install Dependencies:**
   bash
   pip install -r requirements.txt
   

3. **Run the Application:**
   bash
   python app.py
   
   The database `scheduler.db` will be automatically created.

4. **Access the App:**
   - Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - **Sign Up** for a new account to access the dashboard.

## Testing
Run the conflict logic tests:
python test_conflict_logic.py

