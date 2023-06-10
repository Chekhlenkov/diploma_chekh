from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< Updated upstream
=======
    path('api-auth/', include('rest_framework.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
>>>>>>> Stashed changes
]
