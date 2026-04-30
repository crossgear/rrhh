"""
Vistas personalizadas para errores HTTP
"""
from django.shortcuts import render
from django.http import HttpResponseBadRequest


def bad_request(request, exception):
    """Vista para error 400 - Bad Request"""
    return render(request, '404.html', status=400)


def permission_denied(request, exception):
    """Vista para error 403 - Permission Denied"""
    return render(request, '403.html', status=403)


def page_not_found(request, exception):
    """Vista para error 404 - Page Not Found"""
    return render(request, '404.html', status=404)


def server_error(request):
    """Vista para error 500 - Server Error"""
    return render(request, '500.html', status=500)
