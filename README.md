
- `vehicle_maintenance_scheduler/` - Vehicle Maintenance Scheduler API
- `notification_system_design/` - Campus Notification System API

## Prerequisites
- Python 3.8+ installed

## Setup Instructions

1. **Install dependencies**
   Open your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Project 1: Vehicle Maintenance Scheduler**
   Navigate to the project 1 folder and start the server:
   ```bash
   cd vehicle_maintenance_scheduler
   uvicorn main:app --reload --port 8000
   ```
   - Open Swagger UI to test APIs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - *Note: This project automatically creates some dummy data when it starts.*

3. **Run Project 2: Campus Notification System**
   Open a new terminal, navigate to project 2 folder, and start the server on a different port:
   ```bash
   cd notification_system_design
   uvicorn main:app --reload --port 8001
   ```
   - Open Swagger UI to test APIs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
   - *Note: This project uses FastAPI BackgroundTasks to simulate sending notifications without blocking the API response.*


