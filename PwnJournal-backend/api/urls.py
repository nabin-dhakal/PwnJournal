from django.urls import path
from .views import get_writeups, UserProfileView, get_csrf, writeup_detail,get_comments
from core.views import (
    login_view, logout_view, current_user_view,
    register_view, update_user, get_user_profile
)

urlpatterns = [
    path('writeups/', get_writeups, name='writeups'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', current_user_view, name='user_view'),
    path('register/', register_view, name='register_view'),
    path('csrf/', get_csrf, name='csrf_token'),
    path('update/', update_user, name='update_user'),
    path('get-user-profile/', get_user_profile, name='get_user_profile'),
    path('writeups/<int:pk>/',writeup_detail,name='writeup details'),
    path('writeups/<int:pk>/comments',get_comments,name='comments')
]
