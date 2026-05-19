from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from overdue.services import OverdueTaskService


@api_view(['POST'])
def sync_overdue(request):
  count = OverdueTaskService.sync_overdue_tasks()
  return Response({
    'success': True,
    'message': f'Marked {count} task(s) as overdue.',
    'data': {'updated_count': count},
  })


@api_view(['POST'])
def validate_status(request):
  task_id = request.data.get('task_id')
  new_status = request.data.get('new_status')
  user_role = request.data.get('user_role', 'user')

  if not task_id or not new_status:
    return Response({
      'success': False,
      'message': 'task_id and new_status are required.',
    }, status=status.HTTP_400_BAD_REQUEST)

  result = OverdueTaskService.validate_status_change(
    int(task_id), str(new_status), str(user_role)
  )

  return Response({
    'success': result['allowed'],
    'allowed': result['allowed'],
    'message': result['message'],
  })
