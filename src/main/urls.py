# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# REST
from rest_framework_swagger.views import get_swagger_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

API_PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
    path('currency/', include('currency.urls')),
    path('feedback/', include('feedback.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('auth/', include('django.contrib.auth.urls')),

    # API
    path(f'{API_PREFIX}/currency/', include('currency.api.urls')),
    path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# SWAGGER
schema_view = get_swagger_view(title='DOCS')
urlpatterns.append(path(f'{API_PREFIX}/docs/', schema_view))


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2OTIwMTM0LCJqdGkiOiI3MWQxN2ZlNzVmY2Q0YWQ3OTE3NzhhOWFlNGIzY2U3ZSIsInVzZXJfaWQiOjF9.uCmijA_fVqgTc79khhAU_n4o1r8hzRng3XNxnS93r2M

# JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2NDU5MzQxLCJqdGkiOiIxZTJjNjAxMjBmNjc0MmFmYmIwNmFkYjBkYTJkODc1OCIsInVzZXJfaWQiOjh9.PScH_ZKujjlF8zJyGWGVC7_DjxVscm843Aog2YW9838
# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2NDU5MzQxLCJqdGkiOiIxZTJjNjAxMjBmNjc0MmFmYmIwNmFkYjBkYTJkODc1OCIsInVzZXJfaWQiOjh9.PScH_ZKujjlF8zJyGWGVC7_DjxVscm843Aog2YW9838