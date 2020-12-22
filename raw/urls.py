from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('fitness.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = 'fitness.views.handler404'
# handler500 = 'fitness.views.handler500'

admin.site.site_header = "RAW FITNESS"
admin.site.site_title = "RAW FITNESS"
admin.site.site_index_title = "WELCOME TO RAW FITNESS ADMIN PANEL"
