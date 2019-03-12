from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection

from .models import CRUDLog


def logs_list(request):
    crud_logs = CRUDLog.objects.order_by('-created')[:10]

    http_logs = get_http_logs_dict()
    print("\nHTTP logs")
    print(http_logs)

    return render(request, 'logs/logs_list.html', {'http_logs': http_logs, 'crud_logs': crud_logs})


def get_http_logs_dict():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM django_db_logger_statuslog WHERE logger_name = %s ORDER BY create_datetime DESC", ["django.server"])
        return fetchall_to_dict(cursor)


def fetchall_to_dict(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ][:10]
