from django.urls import path
from . import views
from .projects.urls import urlpatterns as projects_urls
from .labels.urls import urlpatterns as labels_urls
from .wikis.urls import urlpatterns as wiki_urls
from .milestones.urls import urlpatterns as milestone_urls
from .tasks.urls import urlpatterns as task_urls
from .organizations.urls import urlpatterns as organization_urls

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
]

urlpatterns += projects_urls
urlpatterns += labels_urls
urlpatterns += wiki_urls
urlpatterns += milestone_urls
urlpatterns += task_urls
urlpatterns += organization_urls

# Error handlers
handler400 = 'app.views.error_400'
handler403 = 'app.views.error_403'
handler404 = 'app.views.error_404'
handler500 = 'app.views.error_500'
