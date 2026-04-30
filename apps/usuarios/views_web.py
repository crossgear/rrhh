from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.views import View


class CustomLoginView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {
            'ldap_enabled': getattr(settings, 'ENABLE_LDAP_AUTH', False),
            'auth_source': request.GET.get('auth_source', 'domain' if getattr(settings, 'ENABLE_LDAP_AUTH', False) else 'local'),
        })

    def post(self, request):
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        auth_source = request.POST.get('auth_source') or ('domain' if getattr(settings, 'ENABLE_LDAP_AUTH', False) else 'local')

        if not username or not password:
            messages.error(request, 'Ingrese usuario y contraseña.')
            return render(request, self.template_name, {
                'ldap_enabled': getattr(settings, 'ENABLE_LDAP_AUTH', False),
                'auth_source': auth_source,
                'username_value': username,
            }, status=400)

        user = None
        backend = None
        if auth_source == 'domain' and getattr(settings, 'ENABLE_LDAP_AUTH', False):
            backend = 'django_auth_ldap.backend.LDAPBackend'
            # Normalizar entradas comunes
            normalized = username
            if '@' in normalized:
                normalized = normalized.split('@', 1)[0]
            if '\\' in normalized:
                normalized = normalized.split('\\', 1)[1]
            username = normalized
        else:
            backend = 'django.contrib.auth.backends.ModelBackend'

        user = authenticate(request, username=username, password=password, backend=backend)

        if user is not None:
            login(request, user, backend=backend)
            return redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)

        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name, {
            'ldap_enabled': getattr(settings, 'ENABLE_LDAP_AUTH', False),
            'auth_source': auth_source,
            'username_value': request.POST.get('username', ''),
        }, status=401)


class CustomLogoutView(LogoutView):
    next_page = 'login'
