
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class AdminMenuHiddenUsersBlockAdminMiddleware:
    """Bloquea acceso directo a /admin/ a usuarios que tienen el menú oculto."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            hidden = {u.lower() for u in getattr(settings, 'ADMIN_MENU_HIDDEN_USERNAMES', set())}
            username = (request.user.username or '').strip().lower()
            if username in hidden:
                pass
                target = reverse('dashboard-index') if getattr(request.user, 'puede_acceder_panel_rrhh', False) else reverse('mi-ficha')
                return redirect(target)
        return self.get_response(request)
