from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("api/v1/", include("src.routes")),
    path('admin/', admin.site.urls),
    #path('shop/', include("src.shop.urls", namespace="shop_app"))
]

if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)