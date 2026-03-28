from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name ='signup'),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('booking', views.booking_view, name='booking'),
    path('<str:booking_id>', views.cancel_booking_view, name='cancel_booking'),
]