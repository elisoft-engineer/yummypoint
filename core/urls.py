from django.contrib import admin
from django.urls import path, include
from . import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #admin urls
    path('admin/', admin.site.urls),
    #core urls
    path('', core_views.Index.as_view(), name="index"),
    path('about/', core_views.About.as_view(), name="about"),
    path('contact/', core_views.Contact.as_view(), name="contact"),
    path('set_theme/<str:theme>/', core_views.set_theme, name='set_theme'),
    path('admin-dashboard/', core_views.AdminDashboard.as_view(), name="admin-dashboard"),
    #app urls
    path('accounts/', include('accounts.urls')),
    path('menu/', include('menu.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)