from django.urls import path

from src.shop import views


app_name = "shop_app"

urlpatterns = [
	path("", views.index_page, name="index-url")	
]