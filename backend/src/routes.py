from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Audio Samurai",
        default_version='v1',
        description="Платформа для аудио",
        contact=openapi.Contact(url="https://www.youtube.com/channel/UCBQsCLHlhKYYIhOJ0eaJ_xA"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

origins = ["*"]

tags_metadata = [
    {
        "name": "src.tracks",
        "description": "Авторизация и регистрация"
    },
    {
        "name": "src.customer",
        "description": "Пользователь и профиль"
    },
   
]

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('audio/', include('src.tracks.urls')),
    path('user/', include('src.customer.urls'))
]