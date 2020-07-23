from django.urls import path
from . import views

app_name = 'thoughts'

urlpatterns = [
    path('', views.list_display, name='list_display'),
    path('tag/<slug:tag_slug>/', views.list_display, name='list_display_by_tag'),  # url that leads to tag page 
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.detail_display, name='detail_display'),
    
]