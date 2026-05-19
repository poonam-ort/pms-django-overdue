from datetime import date

from django.db import transaction
from django.utils import timezone

from users.models import LaravelTask, LaravelUser


class OverdueTaskService:
  """
  Django feature: overdue task handling per assignment spec.
  - Past due_date + status != done -> OVERDUE
  - Overdue tasks cannot move back to in_progress
  - Only admin can close (done) overdue tasks
  """

  @staticmethod
  def sync_overdue_tasks() -> int:
    today = timezone.localdate()
    qs = LaravelTask.objects.exclude(status=LaravelTask.STATUS_DONE).filter(
      due_date__lt=today
    ).exclude(status=LaravelTask.STATUS_OVERDUE)

    count = 0
    with transaction.atomic():
      for task in qs:
        task.status = LaravelTask.STATUS_OVERDUE
        task.save(update_fields=['status'])
        count += 1

    return count

  @staticmethod
  def validate_status_change(task_id: int, new_status: str, user_role: str) -> dict:
    try:
      task = LaravelTask.objects.get(pk=task_id)
    except LaravelTask.DoesNotExist:
      return {'allowed': False, 'message': 'Task not found.'}

    OverdueTaskService.sync_overdue_tasks()
    task.refresh_from_db()

    current = task.status
    new_status = new_status.lower().strip()

    if current == new_status:
      return {'allowed': True, 'message': 'No change.'}

    if current == LaravelTask.STATUS_OVERDUE:
      if new_status == LaravelTask.STATUS_IN_PROGRESS:
        return {
          'allowed': False,
          'message': 'Overdue tasks cannot move back to in_progress.',
        }
      if new_status == LaravelTask.STATUS_DONE:
        if user_role != LaravelUser.ROLE_ADMIN:
          return {
            'allowed': False,
            'message': 'Only admins can close overdue tasks.',
          }
        return {'allowed': True, 'message': 'Overdue task closed by admin.'}

    if new_status == LaravelTask.STATUS_IN_PROGRESS:
      if task.due_date < date.today() and current != LaravelTask.STATUS_DONE:
        return {
          'allowed': False,
          'message': 'Cannot move past-due tasks to in_progress.',
        }

    return {'allowed': True, 'message': 'Status change permitted.'}
