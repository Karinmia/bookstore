from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection


def logs_list(request):
    crud_logs = get_logs_from_db("db")
    http_logs = get_logs_from_db("django.server")

    return render(request, 'logs/logs_list.html', {'http_logs': http_logs, 'crud_logs': crud_logs})


def get_logs_from_db(logger_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM django_db_logger_statuslog WHERE logger_name = %s ORDER BY create_datetime DESC",
                       [logger_name])
        return fetchall_to_dict(cursor)


def fetchall_to_dict(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ][:10]
