from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ your app urls
    path('', include('ASD.urls')),

    # ✅ ADD THIS (LOGIN SYSTEM)
    path('accounts/', include('django.contrib.auth.urls')),
]

# media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)