from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/races/', include('apps.races.urls')),
    path('api/v1/drivers/', include('apps.drivers.urls')),
    path('api/v1/teams/', include('apps.teams.urls')),
    path('api/v1/news/', include('apps.news.urls')),
    path('api/v1/bloggers/', include('apps.bloggers.urls')),

    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
