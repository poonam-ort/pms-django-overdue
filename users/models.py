from django.db import models


class LaravelUser(models.Model):
    """Unmanaged model — maps to Laravel `users` table."""

    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'users'

    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN


class LaravelProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.BigIntegerField(db_column='created_by')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'projects'


class LaravelTask(models.Model):
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_OVERDUE = 'overdue'

    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(LaravelProject, on_delete=models.DO_NOTHING, db_column='project_id')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=20)
    due_date = models.DateField()
    assigned_to = models.BigIntegerField(db_column='assigned_to')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'tasks'
