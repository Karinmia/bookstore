from django.shortcuts import render, get_object_or_404, redirect

from .models import HttpLog, CRUDLog


def logs_list(request):
    http_logs = HttpLog.objects.order_by('-created')
    crud_logs = CRUDLog.objects.order_by('-created')

    return render(request, 'logs/logs_list.html', {'http_logs': http_logs, 'crud_logs': crud_logs})
