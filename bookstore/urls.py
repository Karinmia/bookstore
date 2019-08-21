from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
   openapi.Info(
      title="Bookstore API",
      default_version='v1',
      contact=openapi.Contact(email="karinmia99avr@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/accounts/', include('accounts.urls')),
    path('shop/', include('shop.urls')),
    path('logs/', include('logs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
