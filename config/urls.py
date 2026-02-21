from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/tournaments/', include('apps.tournaments.urls')),
    path('api/v1/race_tracks/', include('apps.race_tracks.urls')),
    path('api/v1/team_stuff/', include('apps.team_stuff.urls')),
    path('api/v1/drivers/', include('apps.drivers.urls')),
    path('api/v1/teams/', include('apps.teams.urls')),
    path('api/v1/news/', include('apps.news.urls')),
    path('api/v1/bloggers/', include('apps.bloggers.urls')),

    # Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)