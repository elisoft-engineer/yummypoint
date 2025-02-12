from django.urls import path, include
from . import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    #admin urls
    path('admin/', include('panel.urls')),
    path('api/', include('api.urls')),
    #core urls
    path('', core_views.Index.as_view(), name="index"),
    path('about/', core_views.About.as_view(), name="about"),
    path('contact/', core_views.Contact.as_view(), name="contact"),
    path('set_theme/<str:theme>/', core_views.set_theme, name='set_theme'),
    #app urls
    path('accounts/', include('accounts.urls')),
    path('menu/', include('menu.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]