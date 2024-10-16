from django.urls import path
from .views import auth_views, main_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('playground/', main_views.playground, name='playground'),

    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout_user, name='logout'),
    path('register/', auth_views.register, name='register'),
    path('activate/<uidb64>/<token>/', auth_views.activate, name='activate'),
]
