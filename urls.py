from django.contrib import admin
from django.urls import path
from rentals import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("book/<int:product_id>/", views.book, name="book"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("booking/<int:booking_id>/status/", views.update_status, name="update_status"),
    path("assistant/", views.assistant, name="assistant"),
]
