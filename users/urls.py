from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='users-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='users-logout'),
    path('register/', views.register, name='users-register'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('profile/<pk>', views.profile, name='profile'),
    # path('profile/<project_pk>', views.userProfile, name='user-profile')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
