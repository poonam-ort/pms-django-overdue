# PMS Django Overdue Service

Handles overdue task logic (shared PostgreSQL database with Laravel).

## Rules implemented

1. Tasks with `due_date` in the past and status not `done` → marked `overdue`
2. Overdue tasks cannot move back to `in_progress`
3. Only `admin` role can close overdue tasks (set to `done`)

## Setup

```bash
cd project_management_system
pip install -r requirements.txt
# Run Laravel migrations first to create tables
python manage.py runserver 8001
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/overdue/sync/ | Mark eligible tasks as overdue |
| POST | /api/overdue/validate-status/ | Validate status transition |

### validate-status body

```json
{
  "task_id": 1,
  "new_status": "done",
  "user_role": "admin"
}
```

## Cron

```bash
python manage.py mark_overdue_tasks
```
