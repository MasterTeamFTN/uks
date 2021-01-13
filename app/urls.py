from django.urls import path
from . import views
from .projects.urls import urlpatterns as projects_urls
from .labels.urls import urlpatterns as labels_urls
from .wikis.urls import urlpatterns as wiki_urls

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
]

urlpatterns += projects_urls
urlpatterns += labels_urls
urlpatterns += wiki_urls
