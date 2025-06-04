# 🚀 Copilot Time Tracker

A Django REST API project for smart, automated time tracking and team management, powered by AI/ML.  
Perfect for IT service teams who want to optimize productivity, automate routine tasks, and gain actionable insights.

---

## 🌟 Features

- **Automated Time Tracking:**  
  Start and stop time entries for tasks with a single click or API call.

- **Predictive Time Management:**  
  Get instant time estimates for tasks using both rule-based logic and a real machine learning model.

- **Activity Monitoring:**  
  Automatically detect and report users who work beyond healthy limits.

- **Leave Management Automation:**  
  Submit leave requests and get instant, conflict-free auto-approval.

- **Time Utilization Analysis:**  
  Visualize and analyze how time is spent across users and tasks.

- **Interactive API Documentation:**  
  Explore and test every endpoint live via Swagger UI.

---

## 🚦 Quickstart

1. **Clone the repository**
    ```sh
    git clone https://github.com/ravikumarmooli9/timetrackingandmonitoringusecase.git
    cd timetrackingandmonitoringusecase
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Train the ML model**
    ```sh
    python tracking/train_model.py
    ```

5. **Run the server**
    ```sh
    python manage.py runserver
    ```

6. **Open Swagger UI**
    - Go to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) in your browser.

---

## 🛠️ API Endpoints & How to Use

| Endpoint                           | Method | What it Does                                              |
|-------------------------------------|--------|----------------------------------------------------------|
| `/api/time-entries/start/`          | POST   | Start tracking time for a task (provide `task` ID)        |
| `/api/time-entries/{id}/stop/`      | POST   | Stop tracking time for a task                             |
| `/api/predict/`                     | POST   | Predict task time (rule-based, send `description`)        |
| `/api/predict-ml/`                  | POST   | Predict task time (ML model, send `features` list)        |
| `/api/activity-monitor/`            | GET    | List users who worked >8 hours today                      |
| `/api/leave-auto/`                  | POST   | Auto-approve leave requests (send user, dates, reason)    |
| `/api/time-utilization/`            | GET    | Show total time spent per user                            |

---

## 📖 Feature-by-Feature Demo Guide

### 1. Automated Time Tracking

- **Start a Time Entry**
    ```json
    POST /api/time-entries/start/
    {
      "task": 1
    }
    ```
    *Starts tracking time for the given task.*

- **Stop a Time Entry**
    ```json
    POST /api/time-entries/{id}/stop/
    ```
    *Stops the running time entry.*

---

### 2. Predictive Time Management

- **Rule-based Prediction**
    ```json
    POST /api/predict/
    {
      "description": "Prepare a detailed monthly report"
    }
    ```
    *Returns an estimated time based on keywords or description length.*

- **ML-based Prediction**
    ```json
    POST /api/predict-ml/
    {
      "features": [120]
    }
    ```
    *Returns an estimated time using a trained ML model.  
    `features` is a list, e.g., `[description_length]`.*

---

### 3. Activity Monitoring

- **Check for Overwork**
    ```http
    GET /api/activity-monitor/
    ```
    *Lists users who have worked more than 8 hours today.*

---

### 4. Leave Management Automation

- **Auto-Approve Leave**
    ```json
    POST /api/leave-auto/
    {
      "user": 1,
      "start_date": "2025-06-01",
      "end_date": "2025-06-02",
      "reason": "Vacation"
    }
    ```
    *Automatically approves leave if there is no conflict.*

---

### 5. Time Utilization Analysis

- **Get Time Utilization**
    ```http
    GET /api/time-utilization/
    ```
    *Shows total time spent per user.*

---

## 🧪 Testing & Demo Tips

- Use Swagger UI for interactive testing: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Prepare some users, tasks, and time entries in advance for a smooth demo.
- For ML predictions, `features` is usually `[description_length]` (e.g., `[120]`).

---

## ⚡ Notes

- **Swagger UI** will show all fields for custom endpoints if you use `@swagger_auto_schema` and input serializers.
- **ML Model:**  
  - Make sure `my_model.pkl` exists in `tracking/` (run `python tracking/train_model.py` if not).
- **Admin-only endpoints:**  
  - `/api/activity-monitor/` and `/api/time-utilization/` require admin privileges.
- **Demo Tips:**  
  - Prepare users, tasks, and time entries in advance for a smooth demo.

---

## 🆘 Troubleshooting

- If you see errors about missing model files, run:
    ```sh
    python tracking/train_model.py
    ```
- If Swagger UI doesn't show fields, restart the server and clear your browser cache.
- For any issues, check server logs and ensure all migrations and model files are in place.

---