from django.core.management.base import BaseCommand

from overdue.services import OverdueTaskService


class Command(BaseCommand):
  help = 'Mark past-due tasks (not DONE) as OVERDUE'

  def handle(self, *args, **options):
    count = OverdueTaskService.sync_overdue_tasks()
    self.stdout.write(self.style.SUCCESS(f'Marked {count} task(s) as overdue.'))
