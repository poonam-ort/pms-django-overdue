from django.http import JsonResponse


def index(request):
    return JsonResponse({
        'app': 'PMS Django Overdue Service',
        'version': '1.0',
        'status': 'running',
        'message': 'Overdue microservice is up. Use /api/overdue/* endpoints.',
        'endpoints': {
            'POST /api/overdue/sync/': 'Mark past-due tasks as overdue',
            'POST /api/overdue/validate-status/': 'Validate task status change',
        },
        'laravel_api': 'http://127.0.0.1:8080/api',
        'frontend': 'http://127.0.0.1:5173',
    })
